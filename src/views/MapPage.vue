<template>
  <div class="MapDashboard">
    <h2>Map</h2>
    <div class="map">
      <NetworkMap />
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
};
</script>

<style>
.MapDashboard {
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
