<template>
  <div class="chart-container">
    <h2>Répartition des Outputs</h2>
    <canvas ref="outputChartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkOutputChart",
  setup() {
    const outputChartCanvas = ref(null);
    let chartInstance = null;

    onMounted(async () => {
      try {
        // Récupération des données depuis l'API Flask
        const response = await axios.get("http://127.0.0.1:5000/api/data");
        const data = response.data;

        // Comptabiliser la répartition des Outputs
        const outputCounts = {};
        data.forEach((item) => {
          outputCounts[item.Output] = (outputCounts[item.Output] || 0) + 1;
        });

        // Préparer les données pour Chart.js
        const labels = Object.keys(outputCounts);
        const values = Object.values(outputCounts);

        // Détruire l'ancienne instance si elle existe
        if (chartInstance) {
          chartInstance.destroy();
        }

        // Initialisation du Pie Chart
        chartInstance = new Chart(outputChartCanvas.value, {
          type: "pie",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Outputs",
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
              title: { display: true, text: "Proportion des Outputs" },
            },
          },
        });
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    });

    return { outputChartCanvas };
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
