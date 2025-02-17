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

    <!-- Conteneur des graphiques et des infos réseau -->
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
      <div class="chart-card" v-if="selectedNetwork">
        <h3>Informations Réseau</h3>
        <p><strong>Utilisateur :</strong> {{ selectedNetwork.ID_user }}</p>
        <p><strong>Ville :</strong> {{ selectedNetwork.Ville }}</p>
        <p><strong>Input :</strong> {{ selectedNetwork.Input }}</p>
        <p>
          <strong>Technologie reseau :</strong>
          {{ selectedNetwork.Technologie_Reseau }}
        </p>
        <p><strong>IP Source :</strong> {{ selectedNetwork.IP_source }}</p>
        <p>
          <strong>IP Destination :</strong> {{ selectedNetwork.IP_destination }}
        </p>
        <p><strong>Serveur :</strong> {{ selectedNetwork.server_name }}</p>
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
    const selectedNetwork = ref(null);

    onMounted(async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/files");
        availableFiles.value = response.data.files;
      } catch (error) {
        console.error("Erreur lors de la récupération des fichiers :", error);
      }
    });

    const fetchSelectedData = async () => {
      if (!selectedFile.value) return;

      try {
        const response = await axios.get(
          `http://localhost:5000/api/data/${selectedFile.value}`
        );
        updateCharts(response.data);
        if (response.data.length > 0) {
          selectedNetwork.value = response.data[0];
        }
      } catch (error) {
        console.error("Erreur lors du chargement des données :", error);
      }
    };

    const updateCharts = (data) => {
      const labels = data.map((item) => item.Moment_du_ping);
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
      selectedNetwork,
    };
  },
};
</script>

<style scoped>
.container {
  .container {
    max-height: 500px; /* Empêche la prise de toute la hauteur */
    overflow-y: auto; /* Permet le scroll si nécessaire */
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
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

canvas {
  width: 100% !important;
  height: 100% !important;
  max-width: 280px;
  max-height: 280px;
}
</style>
