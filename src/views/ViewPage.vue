<template>
  <div class="MapDashboard">
    <h2></h2>
    <div class="charts">
      <JitterChartWithFilter />
    </div>
  </div>
</template>

<script>
import JitterChartWithFilter from "../components/JitterChartWithFilter.vue";

export default {
  name: "MapPage",
  components: {
    JitterChartWithFilter,
  },
};
</script>

<style>
.charts {
  margin: 20px auto; /* Centrage automatique horizontal */
  width: 80%;
  max-width: 1200px;
  display: flex; /* Active Flexbox */
  justify-content: center; /* Centre horizontalement */
  align-items: center; /* Centre verticalement (si nécessaire) */
}
</style>
