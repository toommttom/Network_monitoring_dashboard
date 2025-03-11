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
        <h3>Throuput</h3>
        <canvas ref="throuputChartCanvas"></canvas>
      </div>
    </div>
    <!-- Tableau des statistiques -->
    <div class="stats-table" v-if="filteredData.length">
      <h3>Statistiques</h3>
      <table>
        <thead>
          <tr>
            <th>Métrique</th>
            <th>Min</th>
            <th>Moyenne</th>
            <th>Max</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Jitter (ms)</td>
            <td>{{ minJitter }}</td>
            <td>{{ avgJitter }}</td>
            <td>{{ maxJitter }}</td>
          </tr>
          <tr>
            <td>Latence (ms)</td>
            <td>{{ minLatency }}</td>
            <td>{{ avgLatency }}</td>
            <td>{{ maxLatency }}</td>
          </tr>
          <tr>
            <td>Throuput (kbps)</td>
            <td>{{ minThrouput }}</td>
            <td>{{ avgThrouput }}</td>
            <td>{{ maxThrouput }}</td>
          </tr>
        </tbody>
      </table>
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
    const throuputChartCanvas = ref(null);
    let jitterChartInstance = ref(null);
    let latencyChartInstance = ref(null);
    let throuputChartInstance = ref(null);

    const dataRecords = ref([]);
    const filteredData = ref([]);
    const selectedUser = ref("");
    const selectedVille = ref("");
    const selectedServer = ref("");
    const selectedNetwork = ref(null);

    const uniqueUsers = ref([]);
    const uniqueVilles = ref([]);
    const uniqueServers = ref([]);

    const minJitter = ref(0);
    const avgJitter = ref(0);
    const maxJitter = ref(0);
    const minLatency = ref(0);
    const avgLatency = ref(0);
    const maxLatency = ref(0);
    const minThrouput = ref(0);
    const avgThrouput = ref(0);
    const maxThrouput = ref(0);

    onMounted(async () => {
      try {
        const response = await axios.get("http://172.20.10.3:5000/api/data");
        dataRecords.value = response.data;

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

    const fetchFilteredData = () => {
      filteredData.value = dataRecords.value.filter(
        (item) =>
          (!selectedUser.value || item.ID_user === selectedUser.value) &&
          (!selectedVille.value || item.Ville === selectedVille.value) &&
          (!selectedServer.value || item.server_name === selectedServer.value)
      );

      if (filteredData.value.length > 0) {
        selectedNetwork.value = filteredData.value[0];
        updateStatistics(filteredData.value);
        updateCharts(filteredData.value);
      }
    };

    const updateStatistics = (data) => {
      const values = (key) => data.map((item) => item[key]);
      const calculate = (arr) =>
        arr.length
          ? {
              min: Math.min(...arr),
              avg: (
                arr.reduce((sum, val) => sum + val, 0) / arr.length
              ).toFixed(2),
              max: Math.max(...arr),
            }
          : { min: 0, avg: 0, max: 0 };

      const jitterStats = calculate(values("Jitter"));
      minJitter.value = jitterStats.min;
      avgJitter.value = jitterStats.avg;
      maxJitter.value = jitterStats.max;

      const latencyStats = calculate(values("Latence"));
      minLatency.value = latencyStats.min;
      avgLatency.value = latencyStats.avg;
      maxLatency.value = latencyStats.max;

      const throuputStats = calculate(values("Throuput"));
      minThrouput.value = throuputStats.min;
      avgThrouput.value = throuputStats.avg;
      maxThrouput.value = throuputStats.max;
    };

    const updateCharts = (data) => {
      const labels = data.map((item) => item.Moment_du_ping);
      const jitter = data.map((item) => item.Jitter);
      const latency = data.map((item) => item.Latence);
      const throuput = data.map((item) => item.Throuput);

      const destroyChart = (chartInstance) => {
        if (chartInstance.value) {
          chartInstance.value.destroy();
        }
      };

      destroyChart(jitterChartInstance);
      destroyChart(latencyChartInstance);
      destroyChart(throuputChartInstance);

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

      throuputChartInstance.value = new Chart(throuputChartCanvas.value, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Throuput (kbps)",
              data: throuput,
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
      throuputChartCanvas,
      selectedUser,
      selectedVille,
      selectedServer,
      uniqueUsers,
      uniqueVilles,
      uniqueServers,
      filteredData,
      minJitter,
      avgJitter,
      maxJitter,
      minLatency,
      avgLatency,
      maxLatency,
      minThrouput,
      avgThrouput,
      maxThrouput,
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
  grid-template-columns: repeat(3, minmax(10vw, 1fr));
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
