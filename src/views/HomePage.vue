<template>
  <div class="dashboard">
    <h2>Suivi des performances du réseau</h2>
    
    <div class="charts">
      <LatencyChart />
    </div>

    <div class="charts">
      <JitterChart />
    </div>

    <div class="charts">
      <ThroughputChart />
    </div>
  </div>
</template>

<script>
import LatencyChart from "../components/LatencyChart.vue";
import JitterChart from "../components/JitterChart.vue";
import ThroughputChart from "../components/ThroughputChart.vue";

export default {
  name: "HomePage",
  components: {
    LatencyChart,
    JitterChart,
    ThroughputChart,
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
  min-height: 100vh; /* Utilisation de min-height pour s'adapter au contenu */
}

h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.charts {
  width: 90%;
  max-width: 800px;
  height: 400px; /* Hauteur fixe pour chaque graphique */
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px; /* Espacement entre les graphiques */
}
</style>
