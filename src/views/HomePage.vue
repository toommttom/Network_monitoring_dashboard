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

<style scoped>
.dashboard {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f4f6f8;
  min-height: 100vh;
}

/* Panneau d'information */
.info-panel {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.info-box {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 140px;
}

.info-box h3 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.info-box p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #666;
}

/* Grille des charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 3 colonnes égales */
  gap: 10px;
  width: 90%;
  max-width: 1200px;
  justify-content: center;
  margin-bottom: 20px;
}

.chart-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 350px;
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Section des événements */
.event-container {
  margin-top: 20px;
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 800px;
}

.event-container h3 {
  margin-bottom: 10px;
}

.event-container ul {
  list-style: none;
  padding: 0;
}

.event-container li {
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
}

.event-container li:last-child {
  border-bottom: none;
}

/* Dropdown */
.dropdown-container {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.dropdown-container select {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  cursor: pointer;
}
</style>
