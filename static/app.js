function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; 
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");

  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");

  var url = "/predict_home_price";

  
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      total_sqft: parseFloat(sqft.value),
      bhk: bhk,
      bath: bathrooms,
      location: location.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.estimated_price);
      estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
    })
    .catch((error) => {
      console.error("Error during fetching data:", error);
    });
}

function onPageLoad() {
  console.log("document loaded");
  var url = "/get_location_names";

  
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log("got response for get_location_names request");
      if (data) {
        var locations = data.locations;
        var uiLocations = document.getElementById("uiLocations");
        uiLocations.innerHTML = ""; 
        for (var i = 0; i < locations.length; i++) {
          var option = document.createElement("option");
          option.value = locations[i];
          option.textContent = locations[i];
          uiLocations.appendChild(option);
        }
      }
    })
    .catch((error) => {
      console.error("Error during fetching locations:", error);
    });
}

window.onload = onPageLoad;
