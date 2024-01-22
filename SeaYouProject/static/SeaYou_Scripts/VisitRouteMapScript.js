/* 
Javascript to iterate over the ship's visit's route-waypoints,
put them on the map and add a polyline between them.
Using SnakeAnim plugin
*/

document.addEventListener("DOMContentLoaded", function () {
  let chosenVisit = document.getElementById("chosenVisit");
  let group = [];
  let map = L.map("mapVisits").setView([51.379, 3.6072], 9);
  

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  // Event listener for click on visit links
  document.querySelectorAll(".visit-link").forEach((link) => {
    link.addEventListener("click", async (event) => {
      event.preventDefault();
      const visitId = link.dataset.visitId;
      const shipImo = link.dataset.shipImo;
      const routeId = link.dataset.routeId;
      group = [];
      await clearMap();
      //await clearMarkerList();
      await setChosenVisit(visitId);
      
      fetchRoutesForVisit(visitId, shipImo, routeId);
    });
  });

  const fetchRoutesForVisit = (visitId, shipImo, routeId) => {
    fetch(`/api/get_routes_for_visit/${shipImo}/${visitId}/${routeId}`)
      .then((response) => response.json())
      .then((routes) => {
        updateMapWithRoutes(routes);
      })
      .catch((error) => {
        console.error("Error fetching routes" + error);
      });
  };

  const updateMapWithRoutes = (routes) => {
    for (let i = 0; i < routes.length; i++) {
      const lat = parseFloat(routes[i].waypointid__waypointlatitude);
      const lng = parseFloat(routes[i].waypointid__waypointlongitude);
      const description = routes[i].waypointid__waypointdescription;
      const datetime = routes[i].waypointdt
        ? new Date(routes[i].waypointdt).toLocaleString("en-US")
        : "unknown";
      const dockeddt = routes[i].dockeddt
        ? new Date(routes[i].dockeddt).toLocaleString("en-US")
        : "unknown";
      const popupText = `<strong>${description}</strong> <br/> <strong>Pinged at:</strong> ${datetime}`;

      if (
        typeof lat === "number" &&
        typeof lng === "number" &&
        !isNaN(lat) &&
        !isNaN(lng)
      ) {
        const marker = L.marker([lat, lng]);
        marker.bindPopup(popupText).on("add", () => {
          marker.openPopup();
        });

        group.push(marker);

        if (i < routes.length - 1) {
          const nextRoute = routes[i + 1];
          if (nextRoute) {
            const nextLat = parseFloat(nextRoute.waypointid__waypointlatitude);
            const nextLng = parseFloat(nextRoute.waypointid__waypointlongitude);
            const polyline = L.polyline([
              [lat, lng],
              [nextLat, nextLng],
            ]);

            group.push(polyline);
          }
        } 
      }
    }

    const route = L.featureGroup(group, { snakingPause: 800 });

    map.fitBounds(route.getBounds());

    map.addLayer(route);

    const snake = () => {
      const snake = route.snakeIn();
    };

    snake();
  };


  const setChosenVisit = async (visitId) => {
    while (chosenVisit.hasChildNodes()) {
      chosenVisit.removeChild(chosenVisit.firstChild);
    }
    const textNode = document.createTextNode(`Visit: ${visitId}`);
    chosenVisit.appendChild(textNode);
  };

  const clearMap = async () => {
    map.eachLayer(function (layer) {
      // Check if the layer is a Marker or Polyline
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        map.removeLayer(layer);
      }
    });
  };
});

const toggleTableBody = () => {
  const button = document.getElementById("toggleTableBody");
  const tableBody = document.getElementById("visitsTableBody");
  tableBody.classList.toggle("hidden");
  // Check the current content of the button
  if (button.innerHTML === "↓") {
    // If it's "↓", change it to "↑"
    button.innerHTML = "↑";
    // Add logic for when the arrow is pointing up
    // ...
  } else {
    // If it's not "↓", change it back to "↓"
    button.innerHTML = "↓";
    // Add logic for when the arrow is pointing down
    // ...
  }
}
