<template>
  <div class="chart-container">
    <h2>Inputs</h2>
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
.container {
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

/* Conteneur des checkboxes */
.file-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  background: white;
  padding: 8px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input[type="checkbox"] {
  margin-right: 8px;
}

.load-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 15px;
}

.load-btn:hover {
  background-color: #0056b3;
}

/* Conteneur des graphiques */
.charts-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  width: 100%;
  flex-wrap: wrap; /* Permet d'aller à la ligne si l'écran est trop petit */
}

/* Style uniforme des cartes contenant les graphiques */
.chart-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 30%;
  min-width: 300px;
  height: 350px; /* Hauteur fixe pour uniformiser */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* Empêche le dépassement */
}

/* Ajuster la taille des canvas pour qu'ils ne débordent pas */
canvas {
  width: 100% !important;
  height: 100% !important;
  max-width: 280px; /* Ajustement */
  max-height: 280px;
}
</style>
