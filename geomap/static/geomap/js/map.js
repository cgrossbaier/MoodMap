var center_lat = {{ map.map_center_lat }}
var center_lon = "{{ map.map_center_lon }}"

console.log(center_lat)

var map = L.map('mapImage').setView([center_lat, center_lon], 14);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'cgrossbaier.ojbm8b13',
    accessToken: 'pk.eyJ1IjoiY2dyb3NzYmFpZXIiLCJhIjoiY2lpeDIwdDk5MDAwMnVybTA1NXVwMWd0diJ9.Y5Sdoofp1m9aexIJGwmi_A'
}).addTo(map);

console.log('{{ polygon}}')

//if ('{{ polygon | safe }}' != "None") {
//    L.geoJson({{ polygon | safe}}).addTo(map);
//}

map.on('moveend', function (e) {
    var data = {
        changeType: 'changePosition',
        lat: map.getCenter().lat,
        lon: map.getCenter().lng
    };
    var link = '/geomap/' + '{{ map.id }}' + '/changeMap/';

    $.post(link, data, function () {});
});
map.on('zoomend', function (e) {
    var data = {
        changeType: 'changeZoom',
        zoom: map.getZoom()
    };
    var link = "/geomap/" + '{{ map.id }}' + "/changeMap/";

    $.post(link, data, function () {});
});
$("#buttonResetMap").click(function () {
    var data = {
        changeType: 'resetMap'
    };
    var link = "/geomap/" + '{{ map.id }}' + "/changeMap/";

    $.post(link, data, function () {});
});