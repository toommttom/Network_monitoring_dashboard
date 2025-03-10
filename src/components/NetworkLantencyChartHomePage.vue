<template>
  <div class="container">
    <h2>Évolution de la Latence (Tous les Fichiers)</h2>

    <div class="chart-container">
      <canvas ref="latencyChartCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  name: "NetworkLatencyChart",
  setup() {
    const latencyChartCanvas = ref(null);
    let latencyChartInstance = ref(null);
    const colors = [
      "rgba(255, 99, 132, 1)",
      "rgba(54, 162, 235, 1)",
      "rgba(255, 206, 86, 1)",
      "rgba(75, 192, 192, 1)",
      "rgba(153, 102, 255, 1)",
      "rgba(255, 159, 64, 1)",
    ];

    // Fonction pour récupérer tous les fichiers et leurs données
    const fetchAllData = async () => {
      try {
        const response = await axios.get("http://172.20.10.3:5000/api/files");
        const files = response.data.files;

        const allDataPromises = files.map((file) =>
          axios.get(`http://172.20.10.3:5000/api/data/${file}`).then((res) => ({
            fileName: file,
            data: res.data,
          }))
        );

        const allData = await Promise.all(allDataPromises);
        updateLatencyChart(allData);
      } catch (error) {
        console.error(
          "Erreur lors du chargement des fichiers et données :",
          error
        );
      }
    };

    const getDynamicFontSize = () => {
      return Math.max(5, window.innerWidth * 0.006); // Ajuste dynamiquement (min: 10px)
    };

    // Mise à jour du graphique avec plusieurs fichiers
    const updateLatencyChart = (filesData) => {
      // Récupérer et fusionner tous les timestamps
      let allMoments = filesData.flatMap((file) =>
        file.data.map((item) => item.Moment_du_ping)
      );

      // Trier les timestamps en ordre chronologique et supprimer les doublons
      const labels = [...new Set(allMoments)].sort();

      // Créer les datasets
      const datasets = filesData.map((fileData, index) => ({
        label: fileData.fileName,
        data: labels.map((moment) => {
          const found = fileData.data.find(
            (item) => item.Moment_du_ping === moment
          );
          return found ? found.Latence : null;
        }),
        borderColor: colors[index % colors.length],
        backgroundColor: colors[index % colors.length].replace("1)", "0.2)"),
        fill: true,
        tension: 0.4,
        spanGaps: true, // Ignore les valeurs nulles pour éviter les interruptions de ligne
      }));

      // Détruire l'ancien graphique s'il existe
      if (latencyChartInstance.value) {
        latencyChartInstance.value.destroy();
      }

      // Créer le graphique
      latencyChartInstance.value = new Chart(latencyChartCanvas.value, {
        type: "line",
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          font: {
            size: getDynamicFontSize(), // Appliquer la taille dynamique ici
          },
          plugins: {
            legend: {
              display: true,
              position: "right", // Déplacer la légende à droite
              labels: {
                boxWidth: 20, // Ajuster la taille des carrés de couleur
                padding: 10,
                font: {
                  size: getDynamicFontSize(), // Appliquer la taille dynamique ici
                },
              },
            },
          },
          layout: {
            padding: {
              right: 20, // Laisser un peu d'espace à droite
            },
          },
        },
      });
    };

    // Charger les données au montage du composant
    onMounted(fetchAllData);

    return { latencyChartCanvas };
  },
};
</script>

<style scoped>
/* Style du graphique */
.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 84vw;
  height: 20vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.chart-container .chartjs-legend {
  max-height: 20vh; /* Définit une hauteur max */
  overflow-y: auto; /* Active le scroll vertical */
}
</style>
