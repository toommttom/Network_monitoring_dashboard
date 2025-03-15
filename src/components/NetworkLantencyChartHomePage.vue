<template>
  <div class="container">
    <h2>Évolution de la Latence par Serveur</h2>

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

    // Fonction pour récupérer les données de tous les fichiers
    const fetchAllData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/files");
        const files = response.data.files;

        console.log("📁 Fichiers récupérés :", files);

        const allDataPromises = files.map((file) =>
          axios
            .get(`http://127.0.0.1:5000/api/data/${file}`)
            .then((res) => ({ file, data: res.data })) // Associe le fichier aux données
            .catch((error) => {
              console.error(`❌ Erreur sur ${file}:`, error);
              return { file, data: [] }; // Retourne une liste vide en cas d'erreur pour éviter de bloquer
            })
        );

        const allDataResults = await Promise.allSettled(allDataPromises);

        // Extraire les données valides
        const allData = allDataResults
          .filter((result) => result.status === "fulfilled") // Garder seulement les requêtes réussies
          .flatMap((result) => result.value.data); // Fusionner toutes les données

        console.log("✅ Données combinées :", allData.length, "lignes");

        updateLatencyChart(allData);
      } catch (error) {
        console.error(
          "❌ Erreur lors du chargement des fichiers et données :",
          error
        );
      }
    };

    // Mise à jour du graphique avec toutes les latences
    const updateLatencyChart = (allData) => {
      // Regrouper les données par serveur
      const servers = {};
      allData.forEach((entry) => {
        if (!servers[entry.server_name]) {
          servers[entry.server_name] = [];
        }
        servers[entry.server_name].push({
          moment: entry.Moment_du_ping,
          latence: entry.Latence,
        });
      });

      // Fusionner tous les timestamps en ordre chronologique unique
      let allMoments = [
        ...new Set(allData.map((item) => item.Moment_du_ping)),
      ].sort();

      // Créer les datasets pour chaque serveur
      const datasets = Object.keys(servers).map((server, index) => ({
        label: server,
        data: allMoments.map((moment) => {
          const found = servers[server].find(
            (entry) => entry.moment === moment
          );
          return found ? found.latence : null;
        }),
        borderColor: colors[index % colors.length],
        backgroundColor: colors[index % colors.length].replace("1)", "0.2)"),
        fill: true,
        tension: 0.4,
        spanGaps: false,
      }));

      // Détruire l'ancien graphique s'il existe
      if (latencyChartInstance.value) {
        latencyChartInstance.value.destroy();
      }

      const getDynamicFontSize = () => {
        return Math.max(5, window.innerWidth * 0.006); // Ajuste dynamiquement (min: 10px)
      };
      // Créer le graphique unique avec toutes les séries
      latencyChartInstance.value = new Chart(latencyChartCanvas.value, {
        type: "line",
        data: { labels: allMoments, datasets },
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
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

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
</style>
