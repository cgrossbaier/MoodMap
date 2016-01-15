$(window).load(function(){
        $('#modal_Explanation').modal('show');
    });
    
// Define variables

var buttonAddMarker = document.getElementById("buttonAddMarker");
var buttonEvent = document.getElementById("button-event");
var buttonInfo = document.getElementById("button-info");
var buttonWarning = document.getElementById("button-warning");

L.mapbox.accessToken = 'pk.eyJ1IjoiY2dyb3NzYmFpZXIiLCJhIjoiY2lpeDIwdDk5MDAwMnVybTA1NXVwMWd0diJ9.Y5Sdoofp1m9aexIJGwmi_A';

//var southWest = L.latLng(52.383805, 13.000257),
//    northEast = L.latLng(52.693976, 13.809512),
//    bounds = L.latLngBounds(southWest, northEast);

var map = L.mapbox.map('map', 'mapbox.streets', {
    // set that bounding box as maxBounds to restrict moving the map
    // see full maxBounds documentation:
    // http://leafletjs.com/reference.html#map-maxbounds
//    maxBounds: bounds,
    maxZoom: 19,
    minZoom: 10
}).setView([52.5281028,13.3262337], 10);

// zoom the map to that bounding box
//map.fitBounds(bounds);

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

var markersTemp =  L.layerGroup().addTo(map);
var markers = L.layerGroup().addTo(map);

var markersGeojson = L.mapbox.featureLayer()

map.featureLayer.on('click', function(e) {
        map.panTo(e.layer.getLatLng());
    });

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
    
    saveStatistics("User Location: First time");

    map.setView([crd.latitude, crd.longitude], 14);
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
    saveStatistics("User Location:" + message);
};

navigator.geolocation.getCurrentPosition(success, error, options);

L.control.locate({onLocationError: error, drawCircle: userLocation_Set, icon: 'fa fa-compass'}).addTo(map);

//Function to handle clicks on the category buttons

$("#buttonAddMarker").click(function (ev) {
    saveStatistics("Add Marker");
    $("#button-wrapper-category").css("display", "block");
    $("#buttonAddMarker").css("display", "none");
    $("#buttonAddMarker-clicked").css("display", "inline-block");
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
    $("#buttonAddMarker-clicked").css("display", "none");
    
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
            markersGeojson = L.mapbox.featureLayer()
            .setGeoJSON(JSON.parse(response.event_geoJSON))
            //wait for the layer to be "on", or "loaded", to use a function that will setIcon with an L.icon object
            markersGeojson.eachLayer(function(marker) {
                if (marker.feature.properties.popup !== ""){
                      marker.bindPopup(marker.feature.properties.popup);
                }
            }).addTo(map);            
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
            
            $("#buttonAddMarker-clicked").css("display", "none");
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
//    createMarkers();
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
//            createMarkers()
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

// Explanation
$("#buttonExplanation").click(function(){
    $('#modal_Description').modal('hide');
    $('#modal_Timerange').modal('hide');
    $('#modal_Explanation').modal('show');
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

function createMarkers() {
    bounds = map.getBounds()
    
    x = bounds.getWest()-bounds.getEast();
    y = bounds.getNorth()-bounds.getSouth();

    for (i = 0; i < 20; i++) { 
        marker_Lat = Math.random() * y - y/2 + map.getCenter().lat;
        marker_Lng = Math.random() * x - x/2 + map.getCenter().lng;
        
        random = Math.random();
        markerText = "";
        
        if(random < 0.33) {
            icon = iconEvent_Normal
            markerText = "Event";
        } else if (random > 0.33 & random < 0.66){
            icon = iconWarning_Normal
            markerText = "Warning";
        } else{
             icon = iconInfo_Normal
             markerText = "Info";
        }
    
        marker = L.marker([marker_Lat, marker_Lng], 
            {
            icon: icon
            });
            
        marker.bindPopup(markerText);
        markers.addLayer(marker);

    }
    
    return false
}

