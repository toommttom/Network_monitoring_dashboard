<template>
  <div class="MapDashboard">
    <h2>📍 Suivi du Réseau</h2>

    <div class="info-panel">
      <div class="info-box">
        <h3>{{ markerCount || 0 }}</h3>
        <p>Marqueurs affichés</p>
      </div>
      <div class="info-box">
        <h3>{{ avgLatency.toFixed(2) || "N/A" }} ms</h3>
        <p>Latence moyenne</p>
      </div>
      <div class="info-box">
        <h3>{{ selectedDataset === "traces" ? "Traces" : "Sessions" }}</h3>
        <p>Type de données</p>
      </div>
    </div>

    <div class="map-container">
      <NetworkMap @markers-updated="updateStats" />
    </div>

    <div class="legend">
      <h4>Légende</h4>
      <div class="legend-item">
        <span class="dot high"></span> Latence élevée (> 150 ms)
      </div>
      <div class="legend-item">
        <span class="dot medium"></span> Latence moyenne (80-150 ms)
      </div>
      <div class="legend-item">
        <span class="dot low"></span> Latence faible (&lt; 80 ms)
      </div>
    </div>
  </div>
</template>

<script>
import NetworkMap from "../components/NetworkMap.vue";

export default {
  name: "MapPage",
  components: {
    NetworkMap,
  },
  data() {
    return {
      markerCount: 0,
      avgLatency: 0,
      selectedDataset: "traces",
    };
  },
  methods: {
    updateStats(stats) {
      this.markerCount = stats.count;
      this.avgLatency = stats.avgLatency;
      this.selectedDataset = stats.datasetType;
    },
  },
};
</script>

<style scoped>
/* Style général */
.MapDashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f8f9fa;
}

/* Style du titre */
h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

/* Panneau d'information */
.info-panel {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.info-box {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 120px;
}

.info-box h3 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.info-box p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #666;
}

/* Conteneur de la carte */
.map-container {
  width: 80%;
  max-width: 1200px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Légende */
.legend {
  margin-top: 15px;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.high {
  background: red;
}
.medium {
  background: orange;
}
.low {
  background: green;
}
</style>
