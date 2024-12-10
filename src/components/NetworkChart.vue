<template>
  <div>
    <canvas id="networkChart"></canvas>
  </div>
</template>

<script>
import { Chart } from "chart.js";

export default {
  name: "NetworkChart",
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.chart = new Chart(document.getElementById("networkChart"), {
      type: "line",
      data: {
        labels: ["00:00", "00:05", "00:10"], // Les timestamps de votre réseau
        datasets: [
          {
            label: "Latence (ms)",
            data: [20, 30, 50], // Données simulées
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
          },
        },
      },
    });
  },
};
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
}
</style>
