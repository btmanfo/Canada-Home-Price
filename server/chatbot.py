import os
import json
import numpy as np
import nltk

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader


class ChatbotModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(ChatbotModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

class ChatbotAssistant:
    def __init__(self, intents_path, function_mappings=None):
        self.model = None
        self.intents_path = intents_path

        self.documents = []
        self.vocabulary = []
        self.intents = []
        self.intents_responses = {}

        self.function_mappings = function_mappings

        self.X = None
        self.y = None

    @staticmethod
    def tokenize_and_lemmatize(sentence):
        tokens = nltk.word_tokenize(sentence)
        lemmatizer = nltk.WordNetLemmatizer()

        return [lemmatizer.lemmatize(word.lower()) for word in tokens]

    def bag_of_words(self, tokenized_sentence):
        return np.array([1 if word in tokenized_sentence else 0 for word in self.vocabulary])

    def parse_intents(self):
        if not os.path.exists(self.intents_path):
            raise FileNotFoundError(f"Intent file not found: {self.intents_path}")

        with open(self.intents_path, "r") as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:

            tag = intent["tag"]
            patterns = intent["patterns"]
            responses = intent.get("responses", [])

            if tag not in self.intents:
                self.intents.append(tag)
                self.intents_responses[tag] = responses

            for pattern in patterns:
                tokenized = self.tokenize_and_lemmatize(pattern)
                self.vocabulary.extend(tokenized)
                self.documents.append((tokenized, tag))

        self.vocabulary = sorted(set(self.vocabulary))

    def prepare_data(self):
        bags = []
        indices = []

        for tokenized_sentence, tag in self.documents:
            bow = self.bag_of_words(tokenized_sentence)
            intent_index = self.intents.index(tag)

            bags.append(bow)
            indices.append(intent_index)

        self.X = np.array(bags)
        self.y = np.array(indices)

    def train_model(self, epochs=500, batch_size=8, learning_rate=0.001):
        X_tensor = torch.tensor(self.X, dtype=torch.float32)
        y_tensor = torch.tensor(self.y, dtype=torch.long)

        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = ChatbotModel(self.X.shape[1], len(self.intents))
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            for inputs, labels in loader:
                optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f"Epoch [{epoch+1}/{epochs}] Loss: {loss.item():.4f}")

    def save_model(self, model_path, dims_path):
        torch.save(self.model.state_dict(), model_path)

        with open(dims_path, "w") as f:
            json.dump({
                "input_size": self.X.shape[1],
                "output_size": len(self.intents),
                "vocabulary": self.vocabulary,
                "intents": self.intents
            }, f)

    def load_model(self, model_path, dims_path):
        with open(dims_path, "r") as f:
            dims = json.load(f)

        self.vocabulary = dims["vocabulary"]
        self.intents = dims["intents"]

        self.model = ChatbotModel(dims["input_size"], dims["output_size"])
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def process_message(self, message):
        tokenized = self.tokenize_and_lemmatize(message)
        bow = self.bag_of_words(tokenized)

        bow_tensor = torch.tensor([bow], dtype=torch.float32)

        with torch.no_grad():
            prediction = self.model(bow_tensor)
            probabilities = torch.softmax(prediction, dim=1)
            confidence, index = torch.max(probabilities, dim=1)
        
        confidence = confidence.item()
        if confidence < 0.5:
            return "I'm sorry, I didn't understand that."
        predicted_intent = self.intents[index]

        if self.function_mappings and predicted_intent in self.function_mappings:
            self.function_mappings[predicted_intent]()

        responses = self.intents_responses.get(predicted_intent, [])
        if responses:
            return np.random.choice(responses)

        return "I'm sorry, I didn't understand that."
