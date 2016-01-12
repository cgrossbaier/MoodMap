// Define variables

var typeOfButton = "buttonGood";
var markerColor = document.getElementById("buttonGood").style.backgroundColor;

var setMarker = false;

var color_buttonGood_NotPressed = document.getElementById("buttonGood").style.backgroundColor;
var color_buttonBad_NotPressed = document.getElementById("buttonBad").style.backgroundColor;

var markerColor_Good = "193441";
var markerColor_Bad = "682321";

var buttonGood = document.getElementById("buttonGood");
var buttonBad = document.getElementById("buttonBad");

var color_button_Pressed = "grey";

L.mapbox.accessToken = 'pk.eyJ1IjoiY2dyb3NzYmFpZXIiLCJhIjoiY2lpeDIwdDk5MDAwMnVybTA1NXVwMWd0diJ9.Y5Sdoofp1m9aexIJGwmi_A';

var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([49.910763,2.1681859], 4);

var marker = L.marker();
var buttonClicked;
var buttonSelected;

var iconGood_Small = L.mapbox.marker.icon({'marker-color': markerColor_Good,
                                            'marker-size': 'small'});
var iconGood = L.mapbox.marker.icon({'marker-color': markerColor_Good});
var iconGood_Large = L.mapbox.marker.icon({'marker-color': markerColor_Good,
                                            'marker-size': 'large'});

var iconBad_Small = L.mapbox.marker.icon({'marker-color': markerColor_Bad,
                                            'marker-size': 'small'});
var iconBad = L.mapbox.marker.icon({'marker-color': markerColor_Bad});
var iconBad_Large = L.mapbox.marker.icon({'marker-color': markerColor_Bad,
                                            'marker-size': 'large'});

var markersGood = L.layerGroup().addTo(map);
var markersBad =  L.layerGroup().addTo(map);
var markersTemp =  L.layerGroup().addTo(map);

var userLocation_Set = false;

eventType = "";

//Location Search within Browser

map.locate({setView: true, maxZoom: 16});

var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function success(pos) {
    var crd = pos.coords;
    
    var radius = crd.accuracy / 2;
    
//    createMarkers(crd.latitude, crd.longitude);

    map.setView([crd.latitude, crd.longitude], 14);
    L.circle([crd.latitude, crd.longitude], radius).addTo(map);
    userLocation_Set = true;
};

function error(err) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            message = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            message = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            message = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            message = "An unknown error occurred."
            break;
    }
    console.warn('ERROR(' + err.code + '): ' + message);
};

navigator.geolocation.getCurrentPosition(success, error, options);

L.control.locate({onLocationError: error, drawCircle: userLocation_Set}).addTo(map);

//Create dummy data

function createMarkers(lat, lng, type) {
    var mapCenter_Lat = lat;
    var mapCenter_Lng = lng;


    for (i = 0; i < 100; i++) { 
        marker_Lat = Math.random() * 0.06 - 0.03 + mapCenter_Lat;
        marker_Lng = Math.random() * 0.10 - 0.05 + mapCenter_Lng;
        if(Math.random() > 0.5) {
            marker = L.marker([marker_Lat, marker_Lng], 
                {
                icon: iconGood
                });
            markersGood.addLayer(marker);
        }
         else{
            marker = L.marker([marker_Lat, marker_Lng], 
                {
                icon: iconBad
                });
            markersBad.addLayer(marker);
         }

    }
    
    return false
}

//Function to handle clicks on the category buttons

$(".buttonCategory").click(function (ev) {
    buttonClicked = ev.delegateTarget;
    
    if (setMarker === false){
        buttonClicked.style.backgroundColor = color_button_Pressed;
        buttonClicked.style.borderColor = color_button_Pressed;
        buttonClicked.style.color = "white";

        setMarker = true;
        buttonSelected = buttonClicked;
        
        markersGood.eachLayer(function (layer) {
            layer.setIcon(iconGood_Small);
        });
        markersBad.eachLayer(function (layer) {
            layer.setIcon(iconBad_Small);
        });

        
        if (buttonClicked === buttonGood){
            $(this).find($(".fa")).removeClass('fa-thumbs-up fa-6').addClass('fa-spinner fa-spin');
            icon = iconGood_Large
            eventType = "Good";
        }
        if (buttonClicked === buttonBad){
            $(this).find($(".fa")).removeClass('fa-thumbs-down fa-6').addClass('fa-spinner fa-spin');
            icon = iconBad_Large
            eventType = "Bad";
        }
        
        marker = L.marker([map.getCenter().lat, map.getCenter().lng], 
            {
            icon: icon
            });
        
        markersTemp.addLayer(marker);
    }
    else{
        if (buttonSelected == buttonClicked){
            $('#modalMarker').modal('show');
            setMarker = false;
        }
        else{
            alert("Please save your choice first.")
        }
    }
});

function discardEvent() {
    markersTemp.clearLayers();
    markersGood.eachLayer(function (layer) {
            layer.setIcon(iconGood);
            });
    markersBad.eachLayer(function (layer) {
        layer.setIcon(iconBad);
    });
    if (eventType === "Good"){
        buttonClicked.style.backgroundColor = color_buttonGood_NotPressed;
        buttonClicked.style.borderColor = color_buttonGood_NotPressed;
        $('#buttonGood').find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-thumbs-up fa-6');
    }
    if (eventType === "Bad"){
        buttonClicked.style.backgroundColor = color_buttonBad_NotPressed;
        buttonClicked.style.borderColor = color_buttonBad_NotPressed;
        $('#buttonBad').find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-thumbs-down fa-6');
    }
    $('#modalMarker').modal('hide');
}

function saveEvent() {
    valid_until = $( "#modalMarker_Timerange" ).slider( "value" )
    description = $('textarea#eventDescription').val();
    var data = {eventType: eventType,
               valid_until: valid_until,
               lng: marker.getLatLng().lng,
               lat: marker.getLatLng().lat,
               description: description};
    var link = "/geomap/addEvent/";

    $.post(link, data, function(response){
        if (response.status == 'Okay'){
            marker = L.marker([map.getCenter().lat, map.getCenter().lng], 
            {
            icon: icon
            });
            if (eventType === "Good"){
                buttonClicked.style.backgroundColor = color_buttonGood_NotPressed;
                buttonClicked.style.borderColor = color_buttonGood_NotPressed;
                $('#buttonGood').find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-thumbs-up fa-6');
                markersGood.addLayer(marker);
            }
            if (eventType === "Bad"){
                buttonClicked.style.backgroundColor = color_buttonBad_NotPressed;
                buttonClicked.style.borderColor = color_buttonBad_NotPressed;
                $('#buttonBad').find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-thumbs-down fa-6');
                markersBad.addLayer(marker);
            }
            
            markersGood.eachLayer(function (layer) {
            layer.setIcon(iconGood);
            });
            markersBad.eachLayer(function (layer) {
                layer.setIcon(iconBad);
            });
            markersTemp.clearLayers();
            
            $('#modalMarker').modal('hide');
            
            $( "#modalMarker_Timerange" ).slider( "value" , 60);
            timestamp = new Date(Date.now() + 60 * 1000 * 60);
            timestamp_String = addZero(timestamp.getHours()) + ':' + addZero(timestamp.getMinutes());

            $( "#amount" ).text( "Valid until " + timestamp_String );
            $('#eventDescription').val('');
        }
        else{
            console.log("Error")
            markersTemp.clearLayers();
        }
    });  
};

map.on('move', function (e) {
    if (setMarker){
        var newLatLng = new L.LatLng(map.getCenter().lat, map.getCenter().lng);
        marker.setLatLng(newLatLng);
    }
});

//Search Autocomplete with Google

var defaultBounds = new google.maps.LatLngBounds(
new google.maps.LatLng(map.getBounds().getNorthWest()),
new google.maps.LatLng(map.getBounds().getSouthEast()));

var input = document.getElementById('autocomplete');
var options = {
  bounds: defaultBounds
};

autocomplete = new google.maps.places.Autocomplete(input, options);
autocomplete.addListener('place_changed', onPlaceChanged);

function onPlaceChanged() {
  var place = autocomplete.getPlace();
  if (place.geometry) {
    var newLatLng = new L.LatLng(place.geometry.location.lat(), 
                                 place.geometry.location.lng());
//    createMarkers(place.geometry.location.lat(), place.geometry.location.lng());
    map.panTo(newLatLng);
    map.setZoom(14);
  } else {
    document.getElementById('autocomplete').placeholder = 'Enter a place';
  }
}

$("#buttonSearch").click(function (ev) {
    searchQuery = document.getElementById('autocomplete')
    boundNorthWest_lat = map.getBounds().getNorthWest().lat
    boundNorthWest_lng = map.getBounds().getNorthWest().lng
    boundSouthEast_lat = map.getBounds().getSouthEast().lat
    boundSouthEast_lng = map.getBounds().getSouthEast().lng
    var data = {searchQuery: searchQuery.value,
               boundNorthWest_lat: boundNorthWest_lat,
               boundNorthWest_lng: boundNorthWest_lng,
               boundSouthEast_lat: boundSouthEast_lat,
               boundSouthEast_lng: boundSouthEast_lng};
    var link = "/geomap/searchQuery/";

    $.post(link, data, function(response){
        if (response.status == 'Okay'){
            var newLatLng = new L.LatLng(response.lat, 
                                 response.lng);
            map.panTo(newLatLng);
            map.setZoom(14);
            searchQuery.value = "";
        }
        else{
            console.log("Error")
        }
    });
});


//Slider

function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

$(function() {
    $( "#modalMarker_Timerange" ).slider({
      min: 0,
      max: 260,
      value: 60,
      slide: function( event, ui ) {
        timestamp = new Date(Date.now() + ui.value * 1000 * 60);
        timestamp_String = addZero(timestamp.getHours()) + ':' + addZero(timestamp.getMinutes());
        $( "#amount" ).text( "Valid until " + timestamp_String );
      }
    });

    timestamp = new Date(Date.now() + 60 * 1000 * 60);
    timestamp_String = addZero(timestamp.getHours()) + ':' + addZero(timestamp.getMinutes());
    
    $( "#amount" ).text( "Valid until " + timestamp_String );
        
});

//$(function() {
//    $("#buttonValidity_Down").click(function (ev) {
//    //    console.log($( "#modalMarker_TimeValidity" ).text())
//    //    $( "#modalMarker_TimeValidity" ).html( "3" );
//        $( "#modalMarker_TimeValidity" ).text( "<b>Some</b> new text." );
//    });
//    $("#buttonValidity_Up").click(function (ev) {
//    //    $( "#modalMarker_TimeValidity" ).text( "4" );
//    });
//});        

                           
                           



//
//
//function onMapClick(e) {
//    
//    if (setMarker){
//        var marker = L.marker(e.latlng, 
//            {
//            icon: L.mapbox.marker.icon({
//                'marker-color': markerColor
//            }),
//            draggable: true
//        }).addTo(map);
//        
//        setMarker = false;
//    
//        var buttonSelected = document.getElementById(typeOfButton)
//    
//        if (typeOfButton == "buttonGood"){
//            buttonSelected.style.backgroundColor = color_buttonGood_NotPressed;
//            buttonSelected.style.borderColor = color_buttonGood_NotPressed;
//        }
//        if (typeOfButton == "buttonBad"){
//            buttonSelected.style.backgroundColor = color_buttonBad_NotPressed;
//            buttonSelected.style.borderColor = color_buttonBad_NotPressed;
//        }
//    }
//    
//}
//
//map.on('click', onMapClick);

//
//map.featureLayer.on('click', function(e) {
//        map.panTo(e.layer.getLatLng());
//    });


