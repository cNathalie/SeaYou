const map = L.map("weatherMap").setView([51.282755, 4.336001], 11);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

let stations = JSON.parse(
  document.getElementById("weatherStations_json").textContent
);

stations.forEach((station) => {
  const popupText = `<strong>Station: ${station.location.description
        ? station.location.description
        : station.location.name}</strong> <br/>
        Temp: ${station.tt_10}°C`

  let marker = L.marker([
    station.location.latitude_wgs84,
    station.location.longitude_wgs84,
  ]).addTo(map);
  marker
    .bindPopup(
      popupText
    )
    .on('mouseover', (e) => {
    marker.openPopup()})
});
