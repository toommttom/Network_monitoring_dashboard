<template>
    <div class="chart-container">
      <canvas id="jitterChart"></canvas>
    </div>
  </template>
  
  <script>
  import { onMounted } from "vue";
  import Chart from "chart.js/auto";
  import axios from "axios";
  
  export default {
    name: "JitterChart",
    setup() {
      onMounted(async () => {
        const response = await axios.get("http://localhost:5000/api/data");
        const data = response.data;
        const labels = data.map((item) => item.Date_Performance);
        const jitter = data.map((item) => item.Jitter);
  
        const ctx = document.getElementById("jitterChart").getContext("2d");
        new Chart(ctx, {
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
            scales: {
              x: { title: { display: true, text: "Temps" }, ticks: { autoSkip: true, maxTicksLimit: 6 } },
              y: { title: { display: true, text: "Jitter (ms)" } },
            },
          },
        });
      });
    },
  };
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    max-width: 1000px;
    height: 350px;
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  </style>
  