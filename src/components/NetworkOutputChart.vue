<template>
  <div class="chart-container">
    <canvas ref="outputChartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkOutputChart",
  setup() {
    const outputChartCanvas = ref(null);
    let chartInstance = null;

    // Fonction pour définir dynamiquement la taille de la police
    const getDynamicFontSize = () => {
      return Math.max(12, window.innerWidth * 0.008); // Minimum 12px
    };

    // Fonction pour créer le graphique avec une police dynamique
    const createChart = (canvas, labels, values) => {
      if (!canvas) return;

      return new Chart(canvas, {
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
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                font: { size: getDynamicFontSize() },
              },
            },
            title: {
              display: true,
              text: "Proportion des Outputs",
              font: { size: getDynamicFontSize() },
            },
          },
        },
      });
    };

    // Fonction pour charger les données et initialiser le graphique
    const loadChartData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/data");
        const data = response.data;

        const outputCounts = {};
        if (Array.isArray(data)) {
          for (const item of data) {
            if (item.Output) {
              outputCounts[item.Output] = (outputCounts[item.Output] || 0) + 1;
            }
          }
        } else {
          console.error("Erreur: `data` n'est pas un tableau valide", data);
        }

        const labels = Object.keys(outputCounts);
        const values = Object.values(outputCounts);

        if (chartInstance) {
          chartInstance.destroy();
        }

        chartInstance = createChart(outputChartCanvas.value, labels, values);
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    };

    // Fonction pour mettre à jour la taille de la police au redimensionnement
    const updateChartSize = () => {
      if (chartInstance) {
        chartInstance.options.plugins.title.font.size = getDynamicFontSize();
        chartInstance.options.plugins.legend.labels.font.size =
          getDynamicFontSize();
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

    return { outputChartCanvas };
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
