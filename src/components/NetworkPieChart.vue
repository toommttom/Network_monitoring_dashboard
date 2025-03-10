<template>
  <div class="chart-container">
    <canvas ref="barChartCanvas"></canvas>
  </div>
</template>

<script>
import { onMounted, ref, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkTechnologyChart",
  setup() {
    const barChartCanvas = ref(null);
    let chartInstance = null;

    // Fonction pour obtenir une taille de police dynamique
    const getDynamicFontSize = () => {
      return Math.max(12, window.innerWidth * 0.008); // Minimum 12px
    };

    // Fonction pour créer le graphique avec les tailles dynamiques
    const createChart = (canvas, labels, values) => {
      if (!canvas) return;

      return new Chart(canvas, {
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
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            title: {
              display: true,
              text: "Répartition des Technologies Réseau",
              font: {
                size: getDynamicFontSize(),
              },
            },
          },
          scales: {
            x: {
              ticks: {
                font: {
                  size: getDynamicFontSize(),
                },
              },
            },
            y: {
              beginAtZero: true,
              ticks: {
                font: {
                  size: getDynamicFontSize(),
                },
              },
            },
          },
        },
      });
    };

    // Fonction pour charger les données et initialiser le graphique
    const loadChartData = async () => {
      try {
        const response = await axios.get("http://172.20.10.3:5000/api/data");
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

        chartInstance = createChart(barChartCanvas.value, labels, values);
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    };

    // Fonction pour mettre à jour la taille de la police au redimensionnement
    const updateChartSize = () => {
      if (chartInstance) {
        chartInstance.options.plugins.title.font.size = getDynamicFontSize();
        chartInstance.options.scales.x.ticks.font.size = getDynamicFontSize();
        chartInstance.options.scales.y.ticks.font.size = getDynamicFontSize();
        chartInstance.update();
      }
    };

    // Montage du composant
    onMounted(() => {
      loadChartData();
      window.addEventListener("resize", updateChartSize);
    });

    // Nettoyage avant démontage
    onBeforeUnmount(() => {
      if (chartInstance) {
        chartInstance.destroy();
      }
      window.removeEventListener("resize", updateChartSize);
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
  background-color: white;
  width: 100%;
  height: 60vh; /* Ajuste dynamiquement en fonction de l'écran */
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
