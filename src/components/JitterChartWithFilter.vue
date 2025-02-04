<template>
  <div class="container">
    <h2>Analyse des Performances Réseau</h2>

    <!-- Liste des fichiers avec Boutons Radio -->
    <div class="file-selection">
      <label v-for="file in availableFiles" :key="file" class="radio-label">
        <input
          type="radio"
          v-model="selectedFile"
          :value="file"
          @change="fetchSelectedData"
        />
        {{ file }}
      </label>
    </div>

    <!-- Conteneur des trois graphiques -->
    <div class="charts-container">
      <div class="chart-card">
        <h3>Jitter</h3>
        <canvas ref="jitterChartCanvas"></canvas>
      </div>
      <div class="chart-card">
        <h3>Latence</h3>
        <canvas ref="latencyChartCanvas"></canvas>
      </div>
      <div class="chart-card">
        <h3>Throughput</h3>
        <canvas ref="throughputChartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "JitterChartWithRadio",
  setup() {
    const jitterChartCanvas = ref(null);
    const latencyChartCanvas = ref(null);
    const throughputChartCanvas = ref(null);
    let jitterChartInstance = ref(null);
    let latencyChartInstance = ref(null);
    let throughputChartInstance = ref(null);
    const availableFiles = ref([]);
    const selectedFile = ref(null);

    // Charger la liste des fichiers disponibles au montage
    onMounted(async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/files");
        availableFiles.value = response.data.files;
      } catch (error) {
        console.error("Erreur lors de la récupération des fichiers :", error);
      }
    });

    // Charger les données du fichier sélectionné
    const fetchSelectedData = async () => {
      if (!selectedFile.value) return;

      try {
        const response = await axios.get(
          `http://localhost:5000/api/data/${selectedFile.value}`
        );
        updateCharts(response.data);
      } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
      }
    };

    // Mettre à jour les trois graphiques avec les nouvelles données
    const updateCharts = (data) => {
      const labels = data.map((item) => item.Date_Performance);
      const jitter = data.map((item) => item.Jitter);
      const latency = data.map((item) => item.Latence);
      const throughput = data.map((item) => item.Throuput);

      const destroyChart = (chartInstance) => {
        if (chartInstance.value) {
          chartInstance.value.destroy();
        }
      };

      destroyChart(jitterChartInstance);
      destroyChart(latencyChartInstance);
      destroyChart(throughputChartInstance);

      jitterChartInstance.value = new Chart(jitterChartCanvas.value, {
        type: "line",
        data: {
          labels,
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
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });

      latencyChartInstance.value = new Chart(latencyChartCanvas.value, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Latence (ms)",
              data: latency,
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: true,
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });

      throughputChartInstance.value = new Chart(throughputChartCanvas.value, {
        type: "line",
        data: {
          labels,
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
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    };

    return {
      jitterChartCanvas,
      latencyChartCanvas,
      throughputChartCanvas,
      availableFiles,
      selectedFile,
      fetchSelectedData,
    };
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

/* Conteneur des boutons radio */
.file-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

.radio-label {
  display: flex;
  align-items: center;
  background: white;
  padding: 8px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input[type="radio"] {
  margin-right: 8px;
}

/* Conteneur des graphiques */
.charts-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 100%;
  flex-wrap: nowrap; /* Évite que les graphiques se mettent sur une nouvelle ligne */
}

/* Style uniforme des cartes contenant les graphiques */
.chart-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 30%;
  min-width: 300px;
  height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Ajuster la taille des canvas pour qu'ils ne débordent pas */
canvas {
  width: 100% !important;
  height: 100% !important;
  max-width: 280px;
  max-height: 280px;
}
</style>
