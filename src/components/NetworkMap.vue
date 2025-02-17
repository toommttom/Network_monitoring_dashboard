<template>
  <div>
    <div class="filters">
      <label>Filtrer par technologie :</label>
      <select v-model="selectedTech" @change="updateMap">
        <option value="all">Toutes</option>
        <option v-for="tech in technologies" :key="tech" :value="tech">
          {{ tech }}
        </option>
      </select>
    </div>
    <div id="map"></div>
    <div class="legend">
      <small>
        <div class="legend-item">
          <span class="dot high"></span> Latence élevée
        </div>
        <div class="legend-item">
          <span class="dot medium"></span> Latence moyenne
        </div>
        <div class="legend-item">
          <span class="dot low"></span> Latence faible
        </div>
      </small>
    </div>
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
      markers: [],
      technologies: [],
    };
  },
  mounted() {
    this.initMap();
    this.loadData();
  },
  methods: {
    initMap() {
      this.map = L.map("map").setView([46.603354, 1.888334], 6);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(this.map);
    },
    async loadData() {
      try {
        const response = await axios.get("http://localhost:5000/api/data");
        const data = response.data;
        this.technologies = [
          ...new Set(data.map((item) => item.Technologie_Reseau)),
        ];
        this.updateMarkers(data);
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      }
    },
    updateMarkers(data) {
      if (!this.map) return;
      this.markers.forEach((marker) => this.map.removeLayer(marker));
      this.markers = [];
      const cityCoordinates = {
        PARIS: [48.8566, 2.3522],
        LYON: [45.764, 4.8357],
        MARSEILLE: [43.2965, 5.3698],
        LILLE: [50.6292, 3.0573],
        TOULOUSE: [43.6045, 1.444],
        BORDEAUX: [44.8378, -0.5792],
      };
      const filteredData =
        this.selectedTech === "all"
          ? data
          : data.filter(
              (item) => item.Technologie_Reseau === this.selectedTech
            );
      filteredData.forEach((item) => {
        let coordinates = null;
        if (item.Latitude !== null && item.Longitude !== null) {
          coordinates = [parseFloat(item.Latitude), parseFloat(item.Longitude)];
        } else {
          const city = item.Ville.toUpperCase();
          coordinates = cityCoordinates[city] || null;
        }
        if (coordinates) {
          const marker = L.marker(coordinates).addTo(this.map).bindPopup(`
              <strong>${item.Ville}</strong><br>
              📶 Technologie : ${item.Technologie_Reseau}<br>
              ⏳ Latence : ${item.Latence} ms<br>
              🔄 Jitter : ${item.Jitter} ms<br>
              🚀 Débit : ${item.Throuput} kbps
            `);
          this.markers.push(marker);
        }
      });
    },
    updateMap() {
      axios.get("http://localhost:5000/api/data").then((response) => {
        this.updateMarkers(response.data);
      });
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
</style>
