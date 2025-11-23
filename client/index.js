function onPageLoad(){
    console.log("document loaded")
    var url = "http://127.0.0.1:5000/get_name_element"
    $.get(url, function(data, status){
        console.log("got response for get_location_names request")
        if(data){
            var province = data.province
            var city = data.city
            var home_type = data.home_type
            var smoking_permission = data.smoking_permission
            var uiProvince = document.getElementById('uiProvince')
            var uiCity = document.getElementById('uiCity')
            var uiHomeType = document.getElementById('uiHomeType')
            var uiSmokingPermission = document.getElementById('uiSmokingPermission')

            $('#uiProvince').empty()
            $('#uiCity').empty()
            $('#uiHomeType').empty()
            $('#uiSmokingPermission').empty()

            for(var i in province){
                var opt = new Option(province[i])
                $('#uiProvince').append(opt)
            }

            for(var i in city){
                var opt = new Option(city[i])
                $('#uiCity').append(opt)
            }

            for(var i in home_type){
                var opt = new Option(home_type[i])
                $('#uiHomeType').append(opt)
            }

            for(var i in smoking_permission){
                var opt = new Option(smoking_permission[i])
                $('#uiSmokingPermission').append(opt)
            }
        }
    })
}

function dummies_transformed(){
    var_dummies_transformed = {
        "province": document.getElementById('uiProvince'),
        "city": document.getElementById('uiCity'),
        "home_type": document.getElementById('uiHomeType'),
        "is_smoking": document.getElementById('uiSmokingPermission')
    }
    return var_dummies_transformed
}

function quantifies_variable(){
    quantified_variables = {
        "beds": parseInt(document.getElementById('ui_beds_nbr')),
        "baths": arseFloat(document.getElementById('ui_baths_nbr')),
        "sq_feet": parseInt(document.getElementById('ui_square_feet_nbr')),
        "cats": convert_cats_dogs_to_number(document.getElementById('cats')),
        "dogs": convert_cats_dogs_to_number(document.getElementById('dogs')),
        'nbr_beds': parseInt(document.getElementById('ui_beds_nbr'))
    }
    return quantifies_variables
}

function convert_cats_dogs_to_number(value) {
    if (value === 'True') return 1;
    if (value === 'False') return 0;
    console.log('Erreur de conversion:', value);
    return -1;
}

function on_click_estimate_price() {
    var url = "http://127.0.0.1:5000/predict_home_price";
    $.post(url, {
        "province": document.getElementById('uiProvince').value,
        "city": document.getElementById('uiCity').value,
        "home_type": document.getElementById('uiHomeType').value,
        "smoking_permission": document.getElementById('uiSmokingPermission').value,
        "beds": parseInt(document.getElementById('ui_beds_nbr').value),
        "baths": parseFloat(document.getElementById('ui_baths_nbr').value),
        "sq_feet": parseInt(document.getElementById('ui_square_feet_nbr').value),
        "cats": convert_cats_dogs_to_number(document.getElementById('ui_Is_cats_allowed').value),
        "dogs": convert_cats_dogs_to_number(document.getElementById('ui_is_dogs_allowed').value),
        "nb_beds": parseInt(document.getElementById('ui_beds_nbr').value)
    }, function(data, status) {
        console.log("Prediction response:", data);
        document.getElementById('uiEstimatedPrice').innerHTML = "<b>Prix estimé : $" + data.estimated_price.toLocaleString() + "</b>";
    });
}

function sendChat() {
    let input = document.getElementById("chat_input");
    let msg = input.value.trim();
    if (!msg) return;

    $("#chat_area").append(`<div class="user"><b>You:</b> ${msg}</div>`);
    input.value = "";

    $.ajax({
        url: "http://127.0.0.1:5000/chatbot",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message: msg }),
        success: function(data) {
            $("#chat_area").append(`<div class="bot"><b>Bot:</b> ${data.response}</div>`);
            let chatDiv = document.getElementById("chat_area");
            chatDiv.scrollTop = chatDiv.scrollHeight;
        },
        error: function(err){
            console.error("Erreur AJAX:", err);
        }
    });
}

window.onload = onPageLoad;
