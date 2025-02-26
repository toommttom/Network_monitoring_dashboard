<template>
  <div>
    <div class="filters">
      <!-- Sélecteur entre Traces et Sessions -->
      <label>Afficher :</label>
      <select v-model="selectedDataset" @change="loadData">
        <option value="traces">Traces</option>
        <option value="sessions">Sessions</option>
      </select>

      <!-- Sélecteur de Technologie Réseau -->
      <label>Filtrer par technologie :</label>
      <select v-model="selectedTech" @change="updateMap">
        <option value="all">Toutes</option>
        <option v-for="tech in technologies" :key="tech" :value="tech">
          {{ tech }}
        </option>
      </select>
    </div>

    <div id="map"></div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";

export default {
  name: "NetworkMap",
  data() {
    return {
      map: null,
      selectedTech: "all",
      selectedDataset: "traces", // Valeur par défaut : Traces
      markers: [],
      technologies: [],
    };
  },
  mounted() {
    this.initMap();
    this.loadData();
  },
  methods: {
    // Initialisation de la carte Leaflet
    initMap() {
      this.map = L.map("map").setView([46.603354, 1.888334], 6);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(this.map);
    },

    // Récupération des données depuis l'API selon le dataset sélectionné
    async loadData() {
      try {
        // 📌 CHOISIR L'API EN FONCTION DU DROPDOWN
        const apiUrl =
          this.selectedDataset === "traces"
            ? "http://localhost:5000/api/data"
            : "http://localhost:5000/api/sessions";

        const response = await axios.get(apiUrl);
        const data = response.data;

        // 📌 Mise à jour de la liste des technologies réseau disponibles
        this.technologies = [
          ...new Set(data.map((item) => item.Technologie_Reseau)),
        ];

        // 📌 Met à jour les marqueurs avec les nouvelles données
        this.updateMarkers(data);
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      }
    },

    // Fonction pour récupérer la couleur en fonction de la latence
    getLatencyColor(latency) {
      if (latency >= 150) return "red"; // Latence élevée
      if (latency >= 80) return "orange"; // Latence moyenne
      return "green"; // Latence faible
    },

    // Mise à jour des marqueurs sur la carte en fonction des données
    updateMarkers(data) {
      if (!this.map) return;

      // Supprimer les marqueurs existants AVANT d'ajouter les nouveaux
      this.markers.forEach((marker) => this.map.removeLayer(marker));
      this.markers = [];

      // Coordonnées par défaut pour certaines villes
      const cityCoordinates = {
        PARIS: [48.8566, 2.3522],
        LYON: [45.764, 4.8357],
        MARSEILLE: [43.2965, 5.3698],
        LILLE: [50.6292, 3.0573],
        TOULOUSE: [43.6045, 1.444],
        BORDEAUX: [44.8378, -0.5792],
      };

      // Filtrer les données selon la technologie sélectionnée
      const filteredData =
        this.selectedTech === "all"
          ? data
          : data.filter(
              (item) => item.Technologie_Reseau === this.selectedTech
            );

      // Ajout des marqueurs sur la carte
      filteredData.forEach((item) => {
        let coordinates = null;

        // ⚡ Vérifier si l'élément possède Latitude/Longitude (TRACE)
        if (
          "Latitude" in item &&
          "Longitude" in item &&
          item.Latitude &&
          item.Longitude
        ) {
          coordinates = [parseFloat(item.Latitude), parseFloat(item.Longitude)];
        } else {
          // ⚡ Sinon, prendre la Ville comme fallback (SESSION)
          const city = item.Ville ? item.Ville.toUpperCase() : "PARIS";
          coordinates = cityCoordinates[city] || cityCoordinates["PARIS"];
        }

        if (coordinates) {
          // Déterminer la couleur et la taille du point
          const latencyColor = this.getLatencyColor(item.Latence);
          const size = Math.min(20, Math.max(8, item.Latence / 10)); // Taille entre 8px et 20px

          // Définition de l'icône personnalisée avec couleur et taille dynamique
          const markerIcon = L.divIcon({
            className: "custom-marker",
            html: `<div style="background-color:${latencyColor}; width:${size}px; height:${size}px; border-radius:50%;"></div>`,
            iconSize: [size, size],
          });

          // Création du marqueur sur la carte
          const marker = L.marker(coordinates, { icon: markerIcon }).addTo(
            this.map
          ).bindPopup(`
        <strong>${item.Ville}</strong><br>
        📶 Technologie : ${item.Technologie_Reseau}<br>
        ⏳ Latence : ${item.Latence.toFixed(2)} ms<br>
        🔄 Jitter : ${item.Jitter.toFixed(2)} ms<br>
        🚀 Débit : ${item.Throuput.toFixed(2)} kbps
      `);

          this.markers.push(marker);
        }
      });
      this.$emit("markers-updated", {
        count: this.markers.length,
        avgLatency:
          this.markers.reduce(
            (sum, item) => sum + (item.options.latency || 0),
            0
          ) / Math.max(1, this.markers.length),
        datasetType: this.selectedDataset,
      });
    },

    // Mise à jour de la carte après sélection d'une technologie
    updateMap() {
      this.loadData();
    },
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

.filters {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filters select {
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.legend {
  margin-top: 10px;
  font-size: 0.85em;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.high {
  background: red;
}
.medium {
  background: orange;
}
.low {
  background: green;
}

/* Style des marqueurs personnalisés */
.custom-marker {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
