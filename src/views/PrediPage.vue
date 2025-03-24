<template>
  <div class="dashboard">
    <h1>Analyse des Performances Réseau</h1>
    <div class="charts-row">
      <div class="chart-card">
        <h2>Clustering de la Latence</h2>
        <img
          src="http://localhost:5000/api/clustering-plot"
          alt="Clustering plot"
        />
      </div>
      <div class="chart-card">
        <h2>Prédiction via Random Forest</h2>
        <img
          src="http://localhost:5000/api/random-forest-plot"
          alt="Random forest plot"
        />
        <div class="metrics">
          <p><strong>MAE :</strong> {{ metrics.MAE }} ms</p>
          <p><strong>MSE :</strong> {{ metrics.MSE }} ms²</p>
          <p><strong>R² :</strong> {{ metrics.R2 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PrediPage",
  data() {
    return {
      metrics: {
        MAE: null,
        MSE: null,
        R2: null,
      },
    };
  },
  mounted() {
    fetch("http://localhost:5000/api/random-forest-metrics")
      .then((res) => res.json())
      .then((data) => {
        this.metrics = data;
      })
      .catch((err) => {
        console.error("Erreur lors de la récupération des scores :", err);
      });
  },
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7f9fc;
  min-height: 100vh;
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.charts-row {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.chart-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  width: 45%;
  min-width: 300px;
  transition: transform 0.2s ease;
}

.chart-card:hover {
  transform: translateY(-5px);
}

.chart-card h2 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
  color: #444;
}

.chart-card img {
  width: 100%;
  height: auto;
  border-radius: 0.5rem;
  border: 1px solid #eee;
}

.metrics {
  margin-top: 1rem;
  font-size: 0.95rem;
  color: #333;
  background-color: #f2f4f8;
  padding: 0.8rem 1rem;
  border-radius: 0.5rem;
}
</style>
