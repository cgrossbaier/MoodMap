//$(window).load(function(){
//        $('#modal_Explanation').modal('show');
//    });

// Define variables

var buttonAddMarker = document.getElementById("buttonAddMarker");
var buttonEvent = document.getElementById("button-event");
var buttonInfo = document.getElementById("button-info");
var buttonWarning = document.getElementById("button-warning");

L.mapbox.accessToken = 'pk.eyJ1IjoiY2dyb3NzYmFpZXIiLCJhIjoiY2lpeDIwdDk5MDAwMnVybTA1NXVwMWd0diJ9.Y5Sdoofp1m9aexIJGwmi_A';

var map = L.mapbox.map('map', 'cgrossbaier.ok6pb6m1', {
    // set that bounding box as maxBounds to restrict moving the map
    // see full maxBounds documentation:
    // http://leafletjs.com/reference.html#map-maxbounds
//    maxBounds: bounds,
    maxZoom: 19,
    minZoom: 10,
    zoomControl: false
}).setView([52.5281028,13.3262337], 10);

new L.Control.Zoom({ position: 'bottomleft' }).addTo(map);


// zoom the map to that bounding box
//map.fitBounds(bounds);

var marker = L.marker();
var buttonClicked;

var markerColor;
var setMarker = false;

colorWarning = "BD4932";
//var iconWarning_Normal= L.mapbox.marker.icon({'marker-color': markerColor,
//                                              'marker-size': 'small',
//                                              'marker-symbol': "w"});
var iconWarning_Large= L.mapbox.marker.icon({'marker-color': colorWarning,
                                              'marker-size': 'large',
                                              'marker-symbol': "w"});

colorEvent = "105B63";
//var iconEvent_Normal= L.mapbox.marker.icon({'marker-color': markerColor,
//                                              'marker-size': 'small',
//                                              'marker-symbol': "e"});
var iconEvent_Large= L.mapbox.marker.icon({'marker-color': colorEvent,
                                              'marker-size': 'large',
                                              'marker-symbol': "e"});

colorInfo = "FFD34E";
//var iconInfo_Normal= L.mapbox.marker.icon({'marker-color': markerColor,
//                                              'marker-size': 'small',
//                                              'marker-symbol': "i"});
var iconInfo_Large= L.mapbox.marker.icon({'marker-color': colorInfo,
                                              'marker-size': 'large',
                                              'marker-symbol': "i"});

//var markers = L.layerGroup().addTo(map);
var markersTemp =  L.layerGroup().addTo(map);
var markersGeojson = L.mapbox.featureLayer()

map.featureLayer.on('click', function(e) {
        map.panTo(e.layer.getLatLng());
    });

var userLocation_Set = false;
var locationCircle_Layer = L.layerGroup().addTo(map);
var locationCircle = L.circle();

var eventType = "";
var description = "";

//Location Search within Browser

map.locate({setView: true, maxZoom: 8});
      
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

var lc = L.control.locate({onLocationError: error, icon: 'fa fa-compass', showPopup: false, position: 'bottomleft',}).addTo(map);

// request location update and set location
lc.start();

// For the time now
Date.prototype.timeNow = function () {
     return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes();
}

var newDate = new Date();
$("#timeLastSync").text("Last update: " + newDate.timeNow())

//Function to handle clicks on the category buttons

$("#buttonAddMarker").click(function (ev) {
    saveStatistics("Add Marker");
    $("#button-wrapper-category").css("display", "block");
    $("#buttonAddMarker").css("display", "none");
    $("#buttonAddMarker-clicked").css("display", "inline-block");
});
    
$(".button-category").click(function (ev) {
    buttonClicked = ev.delegateTarget;
    if (buttonEvent === buttonClicked){
        icon = iconEvent_Large;
        eventType = "event";
    }
    if (buttonInfo === buttonClicked){
        icon = iconInfo_Large;
        eventType = "info";
    }
    if (buttonWarning === buttonClicked){
        icon = iconWarning_Large;
        eventType = "warning";
    }
    $("#button-info").css("display", "none");
    $("#button-warning").css("display", "none");
    $("#button-event").css("display", "none");
    $("#buttonAddMarker-setMarker").css("display", "inline-block");
    saveStatistics("Select marker" + eventType);

    marker = L.marker([map.getCenter().lat, map.getCenter().lng], 
        {
        icon: icon
        });

    markersTemp.addLayer(marker);
    setMarker = true;
    }
);
$("#buttonAddMarker-setMarker").click(function (ev) {
    saveStatistics("Set marker" + eventType)
    $('#modal_Description').modal('show');
    $('#eventDescription').focus();
    $("#buttonAddMarker-clicked").css("display", "none");
    $("#buttonAddMarker-setMarker").css("display", "none");
    saveStatistics("Show Description")
    setMarker = false;
    }
);

$('#input-categoryTags').selectize({
    delimiter: ',',
    create: function(input) {
        return {
            value: input,
            text: input
        }
    },
    load: function (query, callback) {
        if (!query.length) return callback();
        var data = {eventType: eventType};
        var link = "/geomap/getCategories/";

        $.post(link, data, function(response){
            if (response.status == 'Okay'){
                if (response.categories !== ''){
                    categories = JSON.parse(response.categories);
                    callback(categories);
                }
                else{
                    callback();
                }
            }}
        );
    }
});

 var $select = $('#input-categoryTags').selectize();
 var categoryTags = $select[0].selectize;


function discardEvent() {
    markersTemp.clearLayers();
    saveStatistics("Discard Event")
    setMarker = false;
    
    $("#buttonAddMarker").css("display", "inline-block");
    $("#buttonAddMarker-clicked").css("display", "none");
    $("#buttonAddMarker-setMarker").css("display", "none");
    
    $("#button-wrapper-category").css("display", "none");
    $("#button-event").css("display", "inline-block");
    $("#button-info").css("display", "inline-block");
    $("#button-warning").css("display", "inline-block");
    
    $("#modalMarker_Timerange" ).slider( "value" , 60);
    $("#amount" ).text( "Valid for 60 minutes");
    $('#eventDescription').val('');
    categoryTags.clear();
    categoryTags.clearOptions();
    
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
    eventType_subCategory = categoryTags.getValue()
    var data = {eventType: eventType,
                eventType_subCategory: eventType_subCategory,
               valid_until: valid_until,
               lng: marker.getLatLng().lng,
               lat: marker.getLatLng().lat,
               description: description};
    var link = "/geomap/addEvent/";
    
    $.post(link, data, function(response){
        if (response.status == 'Okay'){
            saveStatistics("Save Event:" + eventType + " : Successfull")
            newDate = new Date();
            $("#timeLastSync").text("Last update: " + newDate.timeNow())
            markersGeojson = L.mapbox.featureLayer()
            .setGeoJSON(JSON.parse(response.event_geoJSON))
            //wait for the layer to be "on", or "loaded", to use a function that will setIcon with an L.icon object
            markersGeojson.eachLayer(function(marker) {
                if (marker.feature.properties.popup !== ""){
                      marker.bindPopup(marker.feature.properties.popup);
                }
            }).addTo(map);            
            markersTemp.clearLayers();
            
            events = JSON.parse(response.eventListJson);

            var listGroup = document.getElementById("list-group");
            while (listGroup.firstChild) {
                listGroup.removeChild(listGroup.firstChild);
            }
            for (j = 0; j < events.length; j++) {
                addEventToList(events[j].eventType, events[j].description, events[j].duration, events[j].lat, events[j].lng, events[j].eventType_subCategory);
            }

            $("#modalMarker_Timerange" ).slider( "value" , 60);
            $("#amount" ).text( "Valid for 60 minutes");
            $('#eventDescription').val('');
            categoryTags.clear();
            categoryTags.clearOptions();
            
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
//        saveStatistics("Map move with Marker:" + eventType)
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

//var defaultBounds = new google.maps.LatLngBounds(
//new google.maps.LatLng(map.getBounds().getNorthWest()),
//new google.maps.LatLng(map.getBounds().getSouthEast()));
//
//var input = document.getElementById('autocomplete');
//var options = {
//  bounds: defaultBounds
//};
//autocomplete = new google.maps.places.Autocomplete(input, options);
//autocomplete.addListener('place_changed', onPlaceChanged);
//
//function onPlaceChanged() {
//  var place = autocomplete.getPlace();
//  saveStatistics("New search query - Autocomplete: " + $('#autocomplete').val())
//  if (place.geometry) {
//    var newLatLng = new L.LatLng(place.geometry.location.lat(),
//                                 place.geometry.location.lng());
//    map.panTo(newLatLng);
//    map.setZoom(14);
////    createMarkers();
//  } else {
//    document.getElementById('autocomplete').placeholder = 'Enter a place';
//  }
//}

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


//Create list
function addEventToList(type, description, duration, lat, lng, eventType_subCategory) {
    //Create an input type dynamically.
    var element = document.createElement("button");
    var lat = lat;
    var lng = lng;
    //Assign different attributes to the element.
    element.onclick = function() { // Note this is a function
        var newLatLng = new L.LatLng(lat, lng);
        map.panTo(newLatLng);
    };

    element.setAttribute('class', "list-group-item")

    var listSymbol = document.createElement("div");
    var listContent = document.createElement("div");
    var listDistance = document.createElement("div");

    listSymbol.setAttribute('class', "list-symbol")
    listContent.setAttribute('class', "list-content")
    listDistance.setAttribute('class', "list-distance")

    listSymbol.innerHTML = '<i class="fa fa-circle">'
    if (description === ""){
            listContent.innerHTML = "No description"
    }
    else{
        listContent.innerHTML = description
        if (eventType_subCategory !== ""){
            for (i = 0; i < eventType_subCategory.length; i++) {
                if (i === 0) {
                    listContent.innerHTML = listContent.innerHTML + '<div class="popup-tags"><div>'
                }
                listContent.innerHTML = listContent.innerHTML + "<div class='tags'>" + eventType_subCategory[i] + "</div>"
        }
        }
    }
    listDistance.innerHTML = '<i class="fa fa-clock-o"></i><p>' + duration + 'min</p>'

    if (type === "event"){
        listSymbol.style.color = colorEvent;
    }
    if (type === "info"){
        listSymbol.style.color = colorInfo;
    }
    if (type === "warning"){
        listSymbol.style.color = colorWarning;
    }

    element.appendChild(listSymbol);
    element.appendChild(listContent);
    element.appendChild(listDistance);

    var listGroup = document.getElementById("list-group");
    listGroup.appendChild(element);
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

