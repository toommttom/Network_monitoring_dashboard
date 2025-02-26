<template>
  <div class="container">
    <h2>Analyse des Performances Réseau</h2>

    <!-- Dropdown pour sélectionner le fichier -->
    <div class="file-selection">
      <label for="file-select">Sélectionner un fichier :</label>
      <select
        id="file-select"
        v-model="selectedFile"
        @change="fetchSelectedData"
      >
        <option v-for="file in availableFiles" :key="file" :value="file">
          {{ file }}
        </option>
      </select>
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
          <strong>Technologie réseau :</strong>
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
  name: "PerformanceAnalysis",
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

    // Récupérer la liste des fichiers disponibles
    onMounted(async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/files");
        availableFiles.value = response.data.files;
        if (availableFiles.value.length > 0) {
          selectedFile.value = availableFiles.value[0]; // Sélectionner automatiquement le premier fichier
          fetchSelectedData();
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des fichiers :", error);
      }
    });

    // Récupérer les données du fichier sélectionné
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

    // Mettre à jour les graphiques
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
  width: 100%;
  max-width: 1400px; /* Ajuste selon l'écran */
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-left: 220px; /* Décalage pour compenser la largeur de la navbar */
}

/* Centrage du dropdown */
.file-selection {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 15px;
}

.file-selection select {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  cursor: pointer;
}

/* Grille structurée pour aligner les charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 3 colonnes égales */
  gap: 20px; /* Espacement entre les charts */
  width: 100%;
  max-width: 1200px;
  justify-content: center;
  align-items: stretch; /* Alignement vertical */
  margin-bottom: 20px; /* Évite le scroll vertical */
}

/* Style uniforme des cartes contenant les graphiques */
.chart-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 350px; /* Hauteur fixe pour alignement */
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Pour s'assurer que les graphes sont bien contenus */
canvas {
  width: 100% !important;
  height: 100% !important;
  max-width: 280px;
  max-height: 280px;
}
</style>
