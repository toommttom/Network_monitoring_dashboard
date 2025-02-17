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
  margin: 20px 0;
  width: 80%;
  max-width: 1200px;
}
</style>
