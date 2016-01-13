// Define variables

var buttonAddMarker = document.getElementById("buttonAddMarker");
var buttonEvent = document.getElementById("button-event");
var buttonInfo = document.getElementById("button-info");
var buttonWarning = document.getElementById("button-warning");

L.mapbox.accessToken = 'pk.eyJ1IjoiY2dyb3NzYmFpZXIiLCJhIjoiY2lpeDIwdDk5MDAwMnVybTA1NXVwMWd0diJ9.Y5Sdoofp1m9aexIJGwmi_A';

var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([49.910763,2.1681859], 4);

var marker = L.marker();
var buttonClicked;

var markerColor;
var setMarker = false;

markerColor = "BD4932";
var iconWarning_Normal= L.mapbox.marker.icon({'marker-color': markerColor,
                                              'marker-size': 'small',
                                              'marker-symbol': "w"});
var iconWarning_Large= L.mapbox.marker.icon({'marker-color': markerColor,
                                              'marker-size': 'large',
                                              'marker-symbol': "w"});

markerColor = "105B63";
var iconEvent_Normal= L.mapbox.marker.icon({'marker-color': markerColor,
                                              'marker-size': 'small',
                                              'marker-symbol': "e"});
var iconEvent_Large= L.mapbox.marker.icon({'marker-color': markerColor,
                                              'marker-size': 'large',
                                              'marker-symbol': "e"});

markerColor = "FFD34E";
var iconInfo_Normal= L.mapbox.marker.icon({'marker-color': markerColor,
                                              'marker-size': 'small',
                                              'marker-symbol': "i"});
var iconInfo_Large= L.mapbox.marker.icon({'marker-color': markerColor,
                                              'marker-size': 'large',
                                              'marker-symbol': "i"});

//
//var MarkerWarning = L.ExtraMarkers.icon({
//    icon: 'fa-exclamation-circle',
//    markerColor: 'red',
//    shape: 'round',
//    prefix: 'fa'
//  });
//var MarkerEvent = L.ExtraMarkers.icon({
//    icon: 'fa-smile-o',
//    markerColor: 'green',
//    shape: 'round',
//    prefix: 'fa'
//  });
//var MarkerInfo = L.ExtraMarkers.icon({
//    icon: 'fa-info-circle',
//    markerColor: 'purple',
//    shape: 'round',
//    prefix: 'fa'
//  });
//
//var MarkerInfo_DIV = L.divIcon({className: 'MarkerInfo',
//                           iconSize: [60, 60]});

var markersTemp =  L.layerGroup().addTo(map);
var markers = L.layerGroup().addTo(map);

var userLocation_Set = false;

var eventType = "";
var description = "";

var locationCircle = L.circle();

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
    
    saveStatistics("User Location: First time");

    map.setView([crd.latitude, crd.longitude], 14);
//    if (userLocation_Set === false){
//        locationCircle = L.circle([crd.latitude, crd.longitude], radius).addTo(map);
//        userLocation_Set = true;
//        saveStatistics("User Location: First time");
//    }
//    else{
//        map.removeLayer(locationCircle)
//        saveStatistics("User Location");
//    }

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
    saveStatistics("User Location not permitted");
};

navigator.geolocation.getCurrentPosition(success, error, options);

L.control.locate({onLocationError: error, drawCircle: userLocation_Set, icon: 'fa fa-compass'}).addTo(map);

//Function to handle clicks on the category buttons

$("#buttonAddMarker").click(function (ev) {
    saveStatistics("Add Marker");
    $("#button-wrapper-category").css("display", "block");
    $("#buttonAddMarker").css("display", "none");
});
    
$(".button-category").click(function (ev) {
    buttonClicked = ev.delegateTarget;
    
    if (setMarker === false){
        setMarker = true;
        if (buttonEvent === buttonClicked){
            $("#button-info").css("display", "none");
            $("#button-warning").css("display", "none");
            icon = iconEvent_Large;
            eventType = "event";

        }
        if (buttonInfo === buttonClicked){
            $("#button-event").css("display", "none");
            $("#button-warning").css("display", "none");
            icon = iconInfo_Large;
            eventType = "info";
        }
        if (buttonWarning === buttonClicked){
            $("#button-info").css("display", "none");
            $("#button-event").css("display", "none");
            icon = iconWarning_Large;
            eventType = "warning";
        }
        saveStatistics("Select marker" + eventType);
        
        marker = L.marker([map.getCenter().lat, map.getCenter().lng], 
            {
            icon: icon
            });
                
        markersTemp.addLayer(marker);
    }
    else{
        saveStatistics("Set marker" + eventType)
        $('#modal_Description').modal('show');
        $('#eventDescription').focus();
        saveStatistics("Show Description")
        setMarker = false;
    }
});

function discardEvent() {
    markersTemp.clearLayers();
    saveStatistics("Discard Event")
    
    $("#buttonAddMarker").css("display", "inline-block");
    
    $("#button-wrapper-category").css("display", "none");
    $("#button-event").css("display", "inline-block");
    $("#button-info").css("display", "inline-block");
    $("#button-warning").css("display", "inline-block");
    
    $("#modalMarker_Timerange" ).slider( "value" , 60);
    $("#amount" ).text( "Valid for 60 minutes");
    $('#eventDescription').val('');
    
    $("#buttonSaveEvent").find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-check fa-6');
    
    $('#modal_Description').modal('hide');
    $('#modal_Timerange').modal('hide');
}

function showTimerange() {
    saveStatistics("Show Timerange")
    $('#modal_Description').modal('hide');
    $('#modal_Timerange').modal('show');
}

function saveEvent() {
    saveStatistics("Save Event:" + eventType)
    $("#buttonSaveEvent").find($(".fa")).removeClass('fa-check fa-6').addClass('fa-spinner fa-spin');
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
            saveStatistics("Save Event:" + eventType + " : Successfull")        
            marker = L.marker([map.getCenter().lat, map.getCenter().lng], 
            {
            icon: icon
            });
            
            marker.bindPopup(description);
            markers.addLayer(marker);
            
            markersTemp.clearLayers();
            
            $( "#modalMarker_Timerange" ).slider( "value" , 60);
            $("#amount" ).text( "Valid for 60 minutes");
            $('#eventDescription').val('');
            
            $("#buttonAddMarker").css("display", "inline-block");

            $("#button-wrapper-category").css("display", "none");
            $("#button-event").css("display", "inline-block");
            $("#button-info").css("display", "inline-block");
            $("#button-warning").css("display", "inline-block");
            
            $("#buttonSaveEvent").find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-check fa-6');

            $('#modal_Timerange').modal('hide');
            $('#modal_Description').modal('hide');
            $('#modal_Category').modal('hide');
        }
        else{
            console.log("Error")
            $("#buttonSaveEvent").find($(".fa")).removeClass('fa-spinner fa-spin').addClass('fa-check fa-6');
            saveStatistics("Save Event:" + eventType + " : Error")
            markersTemp.clearLayers();
        }
    });  
};

map.on('move', function (e) {
    if (setMarker){
        saveStatistics("Map move with Marker:" + eventType)
        var newLatLng = new L.LatLng(map.getCenter().lat, map.getCenter().lng);
        marker.setLatLng(newLatLng);
    }
    else{
//        saveStatistics("Map move without Marker")
    }
});

map.on('zoomend', function (e) {
    if (setMarker){
        saveStatistics("Map Zoom with Marker:" + eventType)
    }
    else{
//        saveStatistics("Map move without Marker")
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
  saveStatistics("New search query - Autocomplete: " + $('#autocomplete').val())
  if (place.geometry) {
    var newLatLng = new L.LatLng(place.geometry.location.lat(), 
                                 place.geometry.location.lng());
    map.panTo(newLatLng);
    map.setZoom(14);
  } else {
    document.getElementById('autocomplete').placeholder = 'Enter a place';
  }
}

$("#buttonSearch").click(function (ev) {
    searchQuery = document.getElementById('autocomplete')
    saveStatistics("New search query: " + searchQuery)
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
            saveStatistics("New search query: " + searchQuery + ": Successfull")
            var newLatLng = new L.LatLng(response.lat, 
                                 response.lng);
            map.panTo(newLatLng);
            map.setZoom(14);
            searchQuery.value = "";
        }
        else{
            document.getElementById('autocomplete').value = '';
            document.getElementById('autocomplete').placeholder = 'Place not found, enter a place';
            saveStatistics("New search query: " + searchQuery + ": Not found")
        }
    });
});


//Slider

$(function() {
    $( "#modalMarker_Timerange" ).slider({
      min: 0,
      max: 240,
      value: 60,
      step: 30,
      slide: function( event, ui ) {
        $( "#amount" ).text( "Valid for " + ui.value + " minutes" );
        saveStatistics("Slider change: " + eventType + ": Valid for: " + ui.value)
      }
    });

    $( "#amount" ).text( "Valid for 60 minutes" );
        
});

//Statistics

function saveStatistics(statType) {
    var data = {statType: statType,
                   lng: map.getCenter().lng,
                   lat: map.getCenter().lat,
                   zoom: map.getZoom()};
        var link = "/geomap/saveStatistics/";

        $.post(link, data, function(response){
        });
}


//Create dummy data

//function createMarkers(lat, lng, type) {
//    var mapCenter_Lat = lat;
//    var mapCenter_Lng = lng;
//
//
//    for (i = 0; i < 100; i++) { 
//        marker_Lat = Math.random() * 0.06 - 0.03 + mapCenter_Lat;
//        marker_Lng = Math.random() * 0.10 - 0.05 + mapCenter_Lng;
//        if(Math.random() > 0.5) {
//            marker = L.marker([marker_Lat, marker_Lng], 
//                {
//                icon: iconGood
//                });
//            markersGood.addLayer(marker);
//        }
//         else{
//            marker = L.marker([marker_Lat, marker_Lng], 
//                {
//                icon: iconBad
//                });
//            markersBad.addLayer(marker);
//         }
//
//    }
//    
//    return false
//}

