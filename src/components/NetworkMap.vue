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
      <div v-for="(color, index) in gradientColors" :key="index">
        <span class="dot" :style="{ backgroundColor: color }"></span> Latence
        {{ latencyLabels[index] }}
      </div>
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
      gradientColors: [
        "#000003",
        "#00010B",
        "#090720",
        "#110B2D",
        "#160E38",
        "#231151",
        "#2B115E",
        "#3D1271",
        "#451477",
        "#50167B",
        "#5F187F",
        "#671B80",
        "#772189",
        "#7F2582",
        "#8E2981",
        "#982D80",
        "#A02F7F",
        "#B1347A",
        "#BA3878",
        "#CA3E71",
        "#D4456E",
        "#DB4B6A",
        "#E85362",
        "#ED5B5E",
        "#F46C5C",
        "#F87A5C",
        "#FA815E",
        "#FDA167",
        "#FEA56C",
        "#FEB279",
        "#FEB881",
        "#FEC793",
        "#FED7A1",
        "#FEE1AB",
        "#FEF4B6",
        "#FEFDBF",
      ],
      latencyLabels: [
        "< 10 ms",
        "10-20 ms",
        "20-30 ms",
        "30-40 ms",
        "40-50 ms",
        "50-60 ms",
        "60-70 ms",
        "70-80 ms",
        "80-90 ms",
        "90-100 ms",
        "100-110 ms",
        "110-120 ms",
        "120-130 ms",
        "130-140 ms",
        "140-150 ms",
        "150-160 ms",
        "160-170 ms",
        "170-180 ms",
        "180-190 ms",
        "190-200 ms",
        "200-210 ms",
        "210-220 ms",
        "220-230 ms",
        "230-240 ms",
        "240-250 ms",
        "250-260 ms",
        "260-270 ms",
        "270-280 ms",
        "280-290 ms",
        "290-300 ms",
        "300-310 ms",
        "310-320 ms",
        "320-330 ms",
        "330-340 ms",
        "340-350 ms",
        "350-360 ms",
      ],
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
    getColorForLatency(latency) {
      const index = Math.min(
        Math.floor(latency / 10),
        this.gradientColors.length - 1
      );
      return this.gradientColors[index];
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
        const color = this.getColorForLatency(item.Latence);
        const icon = L.divIcon({
          className: "custom-marker",
          html: `<div style="background-color:${color};width:15px;height:15px;border-radius:50%;"></div>`,
        });

        let coordinates = null;

        // Vérifie si latitude et longitude sont présentes dans l'objet
        if (item.Latitude !== null && item.Longitude !== null) {
          coordinates = [parseFloat(item.Latitude), parseFloat(item.Longitude)];
        } else {
          const city = item.Ville.toUpperCase();
          coordinates = cityCoordinates[city] || null;
        }

        if (coordinates) {
          const marker = L.marker(coordinates, { icon }).addTo(this.map)
            .bindPopup(`
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

/* Légende */
.legend {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 5px;
}
</style>
