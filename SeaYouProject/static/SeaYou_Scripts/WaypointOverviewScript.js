
  const map = L.map("map").setView([51.379, 3.6072], 9);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  let waypoints = JSON.parse(
    document.getElementById("waypoints_json").textContent
  );

  waypoints.forEach((waypoint) => {
    let marker = L.marker([
      waypoint.waypointlatitude,
      waypoint.waypointlongitude,
    ]).addTo(map);
    marker.bindPopup(waypoint.waypointdescription).openPopup();
  });
