<template>
  <div id="app">
    <header>
      <h1>Network Monitoring Dashboard</h1>
    </header>
    <div class="main-layout">
      <NavBar />
      <router-view class="content" />
    </div>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>

<style>
header {
  text-align: center;
  margin-top: 20px;
}

h1 {
  font-size: 2rem;
  color: #333;
}

.main-layout {
  display: flex;
  height: calc(100vh - 80px);
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #ecf0f1;
}
</style>
