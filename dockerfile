# Utiliser Python 3.10 pour compatibilité avec TF 2.9.1
FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le dossier model et requirements avant tout
COPY model/ ./model/
COPY requirement.txt .

# Installer les packages Python
RUN pip install --no-cache-dir -r requirement.txt

# Télécharger les ressources NLTK nécessaires
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('punkt_tab')"
# Copier le code de l'application
COPY . .

# Définir le port
ENV PORT=5000
EXPOSE 5000

# Commande par défaut pour lancer le serveur
CMD ["python3", "server/server.py"]
