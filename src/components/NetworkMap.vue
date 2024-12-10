<template>
  <div id="map" style="height: 500px"></div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "NetworkMap",
  mounted() {
    const map = L.map("map").setView([48.8566, 2.3522], 13); // Coordonnées pour Paris (exemple)

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    L.marker([48.8566, 2.3522])
      .addTo(map) // Exemple de marqueur
      .bindPopup("Point réseau")
      .openPopup();
  },
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 500px;
}
</style>
