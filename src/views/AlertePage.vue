<template>
  <div class="alert-container">
    <h2>📢 Fichiers de mesure - Détection d'anomalies</h2>

    <!-- Liste des fichiers -->
    <div class="file-list">
      <div
        v-for="file in analyzedFiles"
        :key="file.name"
        class="file-item"
        :class="{ 'alert-file': file.hasAlert }"
        @click="toggleFileDetails(file.name)"
      >
        {{ file.name }}
      </div>
    </div>

    <!-- Détails du fichier sélectionné -->
    <div v-if="selectedFile" class="file-details">
      <h3>Données du fichier : {{ selectedFile }}</h3>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Technologie Réseau</th>
            <th>Latence (ms)</th>
            <th>Jitter (ms)</th>
            <th>Throuput (kbps)</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in fileData"
            :key="index"
            :class="{ 'alert-row': row.hasAlert }"
          >
            <td>{{ row.Date_Performance }}</td>
            <td>{{ row.Technologie_Reseau }}</td>
            <td :class="{ red: row.Latence > 100 }">{{ row.Latence }}</td>
            <td :class="{ red: row.Jitter > 50 }">{{ row.Jitter }}</td>
            <td :class="{ red: row.Throuput < 1000 }">{{ row.Throuput }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  name: "AlertePage",
  setup() {
    const analyzedFiles = ref([]);
    const selectedFile = ref(null);
    const fileData = ref([]);

    // Charger la liste des fichiers et détecter anomalies
    onMounted(async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/files");
        const files = response.data.files;

        let alertFiles = [];

        // Vérifier chaque fichier pour voir s'il contient des valeurs élevées
        for (let file of files) {
          const res = await axios.get(`http://localhost:5000/api/data/${file}`);
          const data = res.data;

          let hasAlert = data.some(
            (item) =>
              item.Latence > 100 || item.Jitter > 50 || item.Throuput < 1000
          );

          alertFiles.push({ name: file, hasAlert });
        }

        analyzedFiles.value = alertFiles;
      } catch (error) {
        console.error("Erreur lors de la récupération des fichiers :", error);
      }
    });

    // Afficher les détails du fichier sélectionné
    const toggleFileDetails = async (fileName) => {
      if (selectedFile.value === fileName) {
        selectedFile.value = null;
        fileData.value = [];
      } else {
        selectedFile.value = fileName;

        try {
          const response = await axios.get(
            `http://localhost:5000/api/data/${fileName}`
          );
          fileData.value = response.data.map((item) => ({
            Date_Performance: item.Date_Performance,
            Technologie_Reseau: item.Technologie_Reseau,
            Latence: item.Latence,
            Jitter: item.Jitter,
            Throuput: item.Throuput,
            hasAlert:
              item.Latence > 100 || item.Jitter > 50 || item.Throuput < 1000,
          }));
        } catch (error) {
          console.error("Erreur lors du chargement du fichier :", error);
        }
      }
    };

    return {
      analyzedFiles,
      selectedFile,
      fileData,
      toggleFileDetails,
    };
  },
};
</script>

<style scoped>
.alert-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Liste des fichiers en colonne */
.file-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  align-items: center;
}

/* Style de chaque fichier */
.file-item {
  background: white;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: 0.3s;
  text-align: center;
  width: 70%;
}

.file-item:hover {
  background-color: #007bff;
  color: white;
}

/* Surligne les fichiers avec alertes */
.alert-file {
  border: 2px solid red;
  font-weight: bold;
}

/* Détails du fichier */
.file-details {
  background: white;
  padding: 20px;
  margin-top: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  overflow-x: auto;
}

/* Tableau des valeurs */
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #f4f6f8;
}

.red {
  background-color: rgba(255, 0, 0, 0.3);
  font-weight: bold;
}

.alert-row {
  background-color: rgba(255, 0, 0, 0.1);
}
</style>
