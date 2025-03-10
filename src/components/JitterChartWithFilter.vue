<template>
  <div class="container">
    <h2>Analyse des Performances Réseau</h2>

    <!-- Sélection des critères de filtrage -->
    <div class="filter-selection">
      <label>Filtrer par :</label>
      <select v-model="selectedUser" @change="fetchFilteredData">
        <option value="">Utilisateur</option>
        <option v-for="user in uniqueUsers" :key="user" :value="user">
          {{ user }}
        </option>
      </select>

      <select v-model="selectedVille" @change="fetchFilteredData">
        <option value="">Ville</option>
        <option v-for="ville in uniqueVilles" :key="ville" :value="ville">
          {{ ville }}
        </option>
      </select>

      <select v-model="selectedServer" @change="fetchFilteredData">
        <option value="">Serveur</option>
        <option v-for="server in uniqueServers" :key="server" :value="server">
          {{ server }}
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
    // Références pour les graphiques
    const jitterChartCanvas = ref(null);
    const latencyChartCanvas = ref(null);
    const throughputChartCanvas = ref(null);
    let jitterChartInstance = ref(null);
    let latencyChartInstance = ref(null);
    let throughputChartInstance = ref(null);

    // Données et sélection des filtres
    const dataRecords = ref([]); // Contiendra toutes les données reçues
    const selectedUser = ref("");
    const selectedVille = ref("");
    const selectedServer = ref("");
    const selectedNetwork = ref(null);

    // Listes uniques pour les filtres
    const uniqueUsers = ref([]);
    const uniqueVilles = ref([]);
    const uniqueServers = ref([]);

    // Charger toutes les données au montage
    onMounted(async () => {
      try {
        const response = await axios.get("http://172.20.10.3:5000/api/data");
        dataRecords.value = response.data;

        // Extraire les valeurs uniques pour les filtres
        uniqueUsers.value = [
          ...new Set(dataRecords.value.map((item) => item.ID_user)),
        ];
        uniqueVilles.value = [
          ...new Set(dataRecords.value.map((item) => item.Ville)),
        ];
        uniqueServers.value = [
          ...new Set(dataRecords.value.map((item) => item.server_name)),
        ];

        fetchFilteredData();
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      }
    });

    // Fonction pour filtrer les données en fonction des sélections
    const fetchFilteredData = () => {
      let filteredData = dataRecords.value;

      if (selectedUser.value) {
        filteredData = filteredData.filter(
          (item) => item.ID_user === selectedUser.value
        );
      }
      if (selectedVille.value) {
        filteredData = filteredData.filter(
          (item) => item.Ville === selectedVille.value
        );
      }
      if (selectedServer.value) {
        filteredData = filteredData.filter(
          (item) => item.server_name === selectedServer.value
        );
      }

      if (filteredData.length > 0) {
        selectedNetwork.value = filteredData[0]; // Prend le premier élément filtré
        updateCharts(filteredData);
      }
    };

    // Mise à jour des graphiques
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
        options: { responsive: true, maintainAspectRatio: false },
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
        options: { responsive: true, maintainAspectRatio: false },
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
        options: { responsive: true, maintainAspectRatio: false },
      });
    };

    return {
      jitterChartCanvas,
      latencyChartCanvas,
      throughputChartCanvas,
      selectedUser,
      selectedVille,
      selectedServer,
      uniqueUsers,
      uniqueVilles,
      uniqueServers,
      selectedNetwork,
      fetchFilteredData,
    };
  },
};
</script>

<style scoped>
/* 🌟 Conteneur principal */
.container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 🏷️ Titre principal */
h2 {
  font-size: 3vh;
  font-weight: bold;
  color: #333;
  margin-bottom: 2vh;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 🎚️ Conteneur des filtres */
.filter-selection {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1vw;
  background: white;
  padding: 1vh 1vw;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2vh;
}

/* 🏷️ Label des filtres */
.filter-selection label {
  font-size: 2vh;
  font-weight: bold;
  color: #555;
}

/* 📌 Dropdowns */
.filter-selection select {
  padding: 1vh;
  font-size: 2vh;
  border: 0.2vh solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-selection select:hover {
  border-color: #007bff;
}

.filter-selection select:focus {
  outline: none;
  border-color: #0056b3;
}

/* 📈 Grille des charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(4, minmax(10vw, 1fr));
  gap: 10vw;
  width: 90%;
  max-width: 1200px;
  justify-content: center;
  margin-bottom: 2vh;
  translate: -4vw;
}

/* 📊 Style des cartes contenant les graphiques */
.chart-card {
  background: white;
  padding: 4vh;
  border-radius: 1vh;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 30vh;
  width: 15vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Effet au survol */
.chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* 🎨 Titres des graphiques */
.chart-card h3 {
  font-size: 2.5vh;
  font-weight: bold;
  color: #222;
  margin-bottom: 1vh;
}

/* 📊 Taille des graphiques */
canvas {
  width: 100% !important;
  height: 100% !important;
}

/* ℹ️ Informations Réseau */
.chart-card p {
  font-size: 2vh;
  color: #444;
  margin: 4px 0;
}

.chart-card p strong {
  color: #222;
}
</style>
