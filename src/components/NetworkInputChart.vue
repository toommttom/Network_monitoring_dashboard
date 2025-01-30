<template>
  <div class="chart-container">
    <h2>Répartition des Inputs</h2>
    <canvas ref="inputChartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkInputChart",
  setup() {
    const inputChartCanvas = ref(null);
    let chartInstance = null;

    onMounted(async () => {
      try {
        // Récupération des données depuis l'API Flask
        const response = await axios.get("http://127.0.0.1:5000/api/data");
        const data = response.data;

        // Comptabiliser la répartition des Inputs
        const inputCounts = {};
        data.forEach((item) => {
          inputCounts[item.Input] = (inputCounts[item.Input] || 0) + 1;
        });

        // Préparer les données pour Chart.js
        const labels = Object.keys(inputCounts);
        const values = Object.values(inputCounts);

        // Détruire l'ancienne instance si elle existe
        if (chartInstance) {
          chartInstance.destroy();
        }

        // Initialisation du Pie Chart
        chartInstance = new Chart(inputChartCanvas.value, {
          type: "pie",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Inputs",
                data: values,
                backgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56",
                  "#4BC0C0",
                  "#9966FF",
                  "#FF9F40",
                ],
                hoverOffset: 10,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: "bottom" },
              title: { display: true, text: "Proportion des Inputs" },
            },
          },
        });
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    });

    return { inputChartCanvas };
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}
canvas {
  max-width: 100%;
  max-height: 100%;
}
</style>
