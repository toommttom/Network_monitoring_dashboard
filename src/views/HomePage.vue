<template>
  <div class="dashboard">
    <h2>Suivi des performances du réseau</h2>
    <div class="charts">
      <NetworkChart />
    </div>
  </div>
</template>

<script>
import NetworkChart from "../components/NetworkChart.vue";

export default {
  name: "HomePage",
  components: {
    NetworkChart,
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
  height: 100vh; /* Assure un affichage pleine hauteur */
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.charts {
  width: 90%;
  max-width: 800px;
  height: 400px; /* Hauteur fixe pour le graphique */
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
