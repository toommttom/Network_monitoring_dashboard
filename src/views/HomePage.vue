<template>
  <div class="dashboard">
    <h2>Suivi des performances du réseau</h2>

    <div class="charts-container">
      <div class="chart-card"><NetworkPieChart /></div>
      <div class="chart-card"><NetworkInputChart /></div>
      <div class="chart-card"><NetworkOutputChart /></div>
    </div>
  </div>
</template>

<script>
import NetworkPieChart from "../components/NetworkPieChart.vue";
import NetworkInputChart from "../components/NetworkInputChart.vue";
import NetworkOutputChart from "../components/NetworkOutputChart.vue";

export default {
  name: "HomePage",
  components: {
    NetworkPieChart,
    NetworkInputChart,
    NetworkOutputChart,
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
  grid-template-columns: repeat(3, 1fr); /* 3 colonnes de même largeur */
  gap: 20px; /* Espace entre les charts */
  width: 90%;
  max-width: 1200px;
  justify-content: center;
}

/* Assurer la même taille pour chaque graphique */
.chart-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 320px; /* Taille uniforme */
  height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
