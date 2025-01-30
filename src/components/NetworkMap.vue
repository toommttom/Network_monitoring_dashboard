<template>
  <div id="map"></div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";

export default {
  name: "NetworkMap",
  mounted() {
    // Création de la carte centrée sur la France
    const map = L.map("map").setView([46.603354, 1.888334], 6); // Centre de la France

    // Ajout des tuiles OpenStreetMap
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    // Charger les données de l'API Flask
    axios.get("http://localhost:5000/api/data")
      .then((response) => {
        const data = response.data;
        
        // Dictionnaire des villes avec leurs coordonnées
        const cityCoordinates = {
          "PARIS": [48.8566, 2.3522],
          "LYON": [45.764, 4.8357],
          "MARSEILLE": [43.2965, 5.3698],
          "LILLE": [50.6292, 3.0573],
          "TOULOUSE": [43.6045, 1.444],
          "BORDEAUX": [44.8378, -0.5792]
        };

        // Ajouter les marqueurs pour chaque mesure réseau
        data.forEach((item) => {
          const city = item.Ville.toUpperCase(); // Assurer la correspondance
          if (cityCoordinates[city]) {
            L.marker(cityCoordinates[city])
              .addTo(map)
              .bindPopup(`
                <strong>${city}</strong><br>
                📶 Technologie : ${item.Technologie_Reseau}<br>
                ⏳ Latence : ${item.Latence} ms<br>
                🔄 Jitter : ${item.Jitter} ms<br>
                🚀 Débit : ${item.Throuput} kbps
              `);
          }
        });
      })
      .catch((error) => {
        console.error("Erreur lors de la récupération des données :", error);
      });
  },
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 500px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
