<template>
  <div class="dashboard">
    <h2>Suivi des performances du réseau</h2>
    <div class="charts">
      <!-- <NetworkChart /> -->
    </div>
    <div class="map">
      <NetworkMap />
    </div>
  </div>
</template>

<script>
//import NetworkChart from "../components/NetworkChart.vue";
import NetworkMap from "../components/NetworkMap.vue";

export default {
  name: "HomePage",
  components: {
    //NetworkChart,
    NetworkMap,
  },
};
</script>

<style>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.charts,
.map {
  margin: 20px 0;
  width: 80%;
  max-width: 1200px;
}
</style>
