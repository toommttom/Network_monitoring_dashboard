<template>
  <div class="dashboard">
    <h2>Suivi des performances du réseau</h2>

    <div class="charts-container">
      <div class="chart-card"><NetworkPieChart /></div>
      <div class="chart-card"><NetworkInputChart /></div>
      <div class="chart-card"><NetworkOutputChart /></div>
    </div>

    <div class="charts">
      <JitterChartWithFilter />
    </div>

    <!-- <div class="charts">
      <LatencyChart />
    </div>

    <div class="charts">
      <JitterChart />
    </div>

    <div class="charts">
      <ThroughputChart />
    </div> -->
  </div>
</template>

<script>
// import LatencyChart from "../components/LatencyChart.vue";
// import JitterChart from "../components/JitterChart.vue";
// import ThroughputChart from "../components/ThroughputChart.vue";
import NetworkPieChart from "../components/NetworkPieChart.vue";
import NetworkInputChart from "../components/NetworkInputChart.vue";
import NetworkOutputChart from "../components/NetworkOutputChart.vue";
import JitterChartWithFilter from "../components/JitterChartWithFilter.vue";

export default {
  name: "HomePage",
  components: {
    // LatencyChart,
    // JitterChart,
    // ThroughputChart,
    NetworkPieChart,
    NetworkInputChart,
    NetworkOutputChart,
    JitterChartWithFilter,
  },
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f4f6f8;
  min-height: 100vh;
}

/* Conteneur des graphiques en ligne */
.charts-container {
  display: flex;
  flex-wrap: wrap; /* Permet le retour à la ligne si l'écran est petit */
  justify-content: center;
  gap: 20px; /* Espace entre les charts */
  width: 90%;
  max-width: 1200px;
}

/* Style des graphiques */
.chart-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 280px; /* Taille réduite */
  height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
