<template>
  <div class="dashboard">
    <h2>📡 Suivi des Performances du Réseau</h2>

    <!-- Panneau d'infos générales -->
    <div class="info-panel">
      <div class="info-box">
        <h3>📊 {{ totalTests }}</h3>
        <p>Total de Tests</p>
      </div>
      <div class="info-box">
        <h3>⏳ {{ avgLatency.toFixed(2) }} ms</h3>
        <p>Latence Moyenne</p>
      </div>
      <div class="info-box">
        <h3>⚡ {{ maxLatency }} ms</h3>
        <p>Latence Max</p>
      </div>
      <div class="info-box">
        <h3>🌐 {{ selectedDataset === "traces" ? "Traces" : "Sessions" }}</h3>
        <p>Type de Données</p>
      </div>
    </div>

    <!-- Dropdown pour sélectionner le type de données -->
    <div class="dropdown-container">
      <label for="dataset-select">Sélectionner le type de données :</label>
      <select id="dataset-select" v-model="selectedDataset">
        <option value="traces">Traces</option>
        <option value="sessions">Sessions</option>
      </select>
    </div>

    <div class="charts-container">
      <div class="chart-card"><NetworkPieChart /></div>
      <div class="chart-card"><NetworkInputChart /></div>
      <div class="chart-card"><NetworkOutputChart /></div>
      <div class="chart-card"><EventView /></div>
    </div>

    <div class="Latency"><NetworkLantencyChartHomePage /></div>
  </div>
</template>

<script>
import NetworkPieChart from "../components/NetworkPieChart.vue";
import NetworkInputChart from "../components/NetworkInputChart.vue";
import NetworkOutputChart from "../components/NetworkOutputChart.vue";
import EventView from "@/components/EventView.vue";
import NetworkLantencyChartHomePage from "@/components/NetworkLantencyChartHomePage.vue";
import axios from "axios";

export default {
  name: "HomePage",
  components: {
    NetworkPieChart,
    NetworkInputChart,
    NetworkOutputChart,
    EventView,
    NetworkLantencyChartHomePage,
  },
  data() {
    return {
      selectedDataset: "traces",
      totalTests: 0,
      avgLatency: 0,
      maxLatency: 0,
      recentEvents: [],
    };
  },
  mounted() {
    this.fetchStats();
    this.fetchRecentEvents();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get("http://localhost:5000/api/stats");
        this.totalTests = response.data.totalTests;
        this.avgLatency = response.data.avgLatency;
        this.maxLatency = response.data.maxLatency;
      } catch (error) {
        console.error("Erreur lors de la récupération des stats:", error);
      }
    },
    async fetchRecentEvents() {
      try {
        const response = await axios.get("http://localhost:5000/api/events");
        this.recentEvents = response.data.slice(0, 5); // Récupère les 5 derniers événements
      } catch (error) {
        console.error("Erreur lors de la récupération des événements:", error);
      }
    },
  },
};
</script>

### **🎨 Mise à jour du CSS pour un affichage adaptatif** ```css
<style scoped>
/* 🌍 La page entière s'adapte à la taille de l'écran */
.dashboard {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2vh;
  background-color: white;
  min-height: 100vh;
}

/* 🏷️ Titre principal */
h2 {
  font-size: 3vh;
  font-weight: bold;
  color: #333;
  margin-bottom: 2vh;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 📊 Panneau d'information */
.info-panel {
  display: flex;
  justify-content: center;
  gap: 1.5vw;
  margin-bottom: 2vh;
  width: 90%;
  flex-wrap: wrap;
}

.info-box {
  background: white;
  padding: 1vh;
  border-radius: 1vh;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 12vw;
  max-width: 12vw;
  font-size: 2vh;
}

/* 📌 Texte dans les boîtes d'info */
.info-box h3 {
  margin: 0;
  font-size: 2vh;
  font-weight: bold;
}

.info-box p {
  margin: 1vh 0 0;
  font-size: 1.5vh;
  color: #666;
}

/* 📈 Grille des charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(4, minmax(10vw, 1fr));
  gap: 10vw;
  width: 90%;
  max-width: 1200px;
  justify-content: center;
  margin-bottom: 2vh;
  translate: -4vw;
}

/* 📊 Style des cartes contenant les graphiques */
.chart-card {
  background: white;
  padding: 4vh;
  border-radius: 1vh;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 30vh;
  width: 15vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 🏗️ Ajustement au survol */
.chart-card:hover {
  transform: translateY(-1vh);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* 📊 Taille des graphiques */
canvas {
  width: 100% !important;
  height: 100% !important;
  max-width: 35vw;
  max-height: 30vh;
}

/* 🔽 Dropdown */
.dropdown-container {
  margin-bottom: 2vh;
  display: flex;
  align-items: center;
  gap: 1vw;
}

.dropdown-container select {
  padding: 1vh;
  border-radius: 1vh;
  border: 2px solid #ccc;
  font-size: 2vh;
  cursor: pointer;
}
</style>
