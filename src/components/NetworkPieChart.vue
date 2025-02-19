<template>
  <div class="chart-container">
    <h2>Technologies Réseau</h2>
    <canvas ref="barChartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkTechnologyChart",
  setup() {
    const barChartCanvas = ref(null);
    let chartInstance = null;

    onMounted(async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/data");
        const data = response.data;

        const technologieCounts = {};
        data.forEach((item) => {
          technologieCounts[item.Technologie_Reseau] =
            (technologieCounts[item.Technologie_Reseau] || 0) + 1;
        });

        const labels = Object.keys(technologieCounts);
        const values = Object.values(technologieCounts);

        if (chartInstance) {
          chartInstance.destroy();
        }

        chartInstance = new Chart(barChartCanvas.value, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Technologies Réseau",
                data: values,
                backgroundColor: "#36A2EB",
                borderColor: "#1E88E5",
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: false },
              title: {
                display: true,
                text: "Répartition des Technologies Réseau",
              },
            },
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    });

    return { barChartCanvas };
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f4f6f8;
  border-radius: 8px;
  width: 90%;
  max-width: 1200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

canvas {
  width: 100% !important;
  height: 100% !important;
  max-width: 600px;
  max-height: 400px;
}
</style>
