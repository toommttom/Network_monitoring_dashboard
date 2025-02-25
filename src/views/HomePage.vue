<template>
  <div class="dashboard">
    <h2>Suivi des performances du réseau</h2>

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

export default {
  name: "HomePage",
  components: {
    NetworkPieChart,
    NetworkInputChart,
    NetworkOutputChart,
    EventView,
    NetworkLantencyChartHomePage,
  },
};
</script>

<style scoped>
.dashboard {
  flex: 1; /* Permet de prendre tout l'espace disponible */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f4f6f8;
  min-height: 100vh;
}

/* Utilisation d'une grille pour aligner les trois premiers charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 3 colonnes de même largeur */
  gap: 10px; /* Espace entre les charts */
  width: 90%;
  max-width: 1200px;
  justify-content: center;
  margin-bottom: 5px;
}

/* Assurer la même taille pour chaque graphique */
.chart-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 350px; /* Taille uniforme */
  height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.Lantency {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}

/* Style du dropdown */
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
