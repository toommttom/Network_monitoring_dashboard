<template>
  <div class="dashboard-container">
    <h2>Suivi des performances du réseau</h2>

    <div class="charts-wrapper">
      <div class="chart-container">
        <canvas id="latencyChart"></canvas>
      </div>

      <div class="chart-container">
        <canvas id="jitterChart"></canvas>
      </div>

      <div class="chart-container">
        <canvas id="throughputChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkCharts",
  setup() {
    const latencyChart = ref(null);
    const jitterChart = ref(null);
    const throughputChart = ref(null);

    onMounted(async () => {
      try {
        // Récupération des données depuis l'API Flask
        const response = await axios.get("http://localhost:5000/api/data");
        const data = response.data;

        // Transformation des données
        const labels = data.map((item) => item.Date_Performance);
        const latence = data.map((item) => item.Latence);
        const jitter = data.map((item) => item.Jitter);
        const throughput = data.map((item) => item.Throuput);

        const commonOptions = {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: { display: true, text: "Temps" },
              ticks: {
                maxRotation: 20, // Rotation plus faible des labels X
                minRotation: 20,
                autoSkip: true,
                maxTicksLimit: 6, // Réduire le nombre de labels affichés
              },
            },
            y: {
              title: { display: true, text: "Valeurs" },
            },
          },
        };

        // 🟢 Initialisation du graphique de Latence
        const latencyCtx = document.getElementById("latencyChart").getContext("2d");
        latencyChart.value = new Chart(latencyCtx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Latence (ms)",
                data: latence,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                fill: true,
                tension: 0.4,
              },
            ],
          },
          options: { ...commonOptions, plugins: { title: { display: true, text: "Latence" } } },
        });

        // 🔴 Initialisation du graphique de Jitter
        const jitterCtx = document.getElementById("jitterChart").getContext("2d");
        jitterChart.value = new Chart(jitterCtx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Jitter (ms)",
                data: jitter,
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                fill: true,
                tension: 0.4,
              },
            ],
          },
          options: { ...commonOptions, plugins: { title: { display: true, text: "Jitter" } } },
        });

        // 🔵 Initialisation du graphique de Throughput
        const throughputCtx = document.getElementById("throughputChart").getContext("2d");
        throughputChart.value = new Chart(throughputCtx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Throughput (kbps)",
                data: throughput,
                borderColor: "rgba(54, 162, 235, 1)",
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                fill: true,
                tension: 0.4,
              },
            ],
          },
          options: { ...commonOptions, plugins: { title: { display: true, text: "Throughput" } } },
        });

      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      }
    });

    return { latencyChart, jitterChart, throughputChart };
  },
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  overflow: hidden; /* Empêche le dépassement */
  padding: 20px;
}

h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.charts-wrapper {
  display: flex;
  flex-direction: column;
  gap: 30px; /* Espacement entre les graphiques */
  width: 90%;
  max-width: 1200px; /* Empêche que ça devienne trop large */
}

.chart-container {
  width: 100%;
  max-width: 1000px; /* Empêche le dépassement horizontal */
  height: 350px; /* Ajustement de la hauteur */
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
