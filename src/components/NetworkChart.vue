<template>
  <div>
    <canvas id="networkChart"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkChart",
  setup() {
    const chartInstance = ref(null);

    onMounted(async () => {
      // Récupération des données depuis l'API Flask
      const response = await axios.get("http://localhost:5000/api/data");
      const data = response.data;

      // Transformation des données pour Chart.js
      const labels = data.map((item) => item.Date_Performance);
      const latence = data.map((item) => item.Latence);
      const jitter = data.map((item) => item.Jitter);
      const throughput = data.map((item) => item.Throuput);

      // Configuration du graphique
      const config = {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Latence (ms)",
              data: latence,
              borderColor: "rgba(75, 192, 192, 1)",
              fill: false,
            },
            {
              label: "Jitter (ms)",
              data: jitter,
              borderColor: "rgba(255, 99, 132, 1)",
              fill: false,
            },
            {
              label: "Throughput (kbps)",
              data: throughput,
              borderColor: "rgba(54, 162, 235, 1)",
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false, // Permet d'ajuster la taille selon le conteneur
          plugins: {
            title: {
              display: true,
              text: "Network Performance Monitoring",
              font: {
                size: 20,
              },
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Temps",
              },
            },
            y: {
              title: {
                display: true,
                text: "Valeurs",
              },
            },
          },
        },
      };

      // Initialisation de Chart.js
      const ctx = document.getElementById("networkChart").getContext("2d");
      chartInstance.value = new Chart(ctx, config);
    });

    return { chartInstance };
  },
};
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
