<template>
  <div class="chart-container">
    <h2>Répartition des Technologies Réseau</h2>
    <canvas ref="pieChartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkPieChart",
  setup() {
    const pieChartCanvas = ref(null);
    let chartInstance = null;

    onMounted(async () => {
      try {
        // Récupération des données depuis l'API Flask
        const response = await axios.get("http://127.0.0.1:5000/api/data");
        const data = response.data;

        // Comptabiliser la répartition des technologies réseau
        const technologieCounts = {};
        data.forEach((item) => {
          technologieCounts[item.Technologie_Reseau] =
            (technologieCounts[item.Technologie_Reseau] || 0) + 1;
        });

        // Préparer les données pour Chart.js
        const labels = Object.keys(technologieCounts);
        const values = Object.values(technologieCounts);

        // Détruire l'ancienne instance si elle existe (évite les bugs en réactualisant le composant)
        if (chartInstance) {
          chartInstance.destroy();
        }

        // Initialisation du Pie Chart
        chartInstance = new Chart(pieChartCanvas.value, {
          type: "pie",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Technologies Réseau",
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
              legend: {
                position: "bottom",
              },
              title: {
                display: true,
                text: "Proportion des Technologies Réseau",
              },
            },
          },
        });
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    });

    return { pieChartCanvas };
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 600px;
  margin: auto;
}
canvas {
  max-width: 100%;
  height: auto;
}
</style>
