<template>
  <div id="navbar">
    <nav class="vertical-navbar">
      <ul>
        <li>
          <router-link to="/" active-class="active">Home</router-link>
        </li>
        <li>
          <router-link to="/map" active-class="active">Map</router-link>
        </li>
        <li>
          <router-link to="/charts" active-class="active">Alerte</router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: "NavBar",
};
</script>

<style scoped>
#navbar {
  display: flex;
  height: 100vh;
  margin: 0;
}

.vertical-navbar {
  width: 200px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}

.vertical-navbar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.vertical-navbar li {
  margin: 10px 0;
}

.vertical-navbar a {
  color: white;
  text-decoration: none;
  font-size: 18px;
}

.vertical-navbar a.active {
  font-weight: bold;
  border-left: 4px solid #3498db;
  padding-left: 10px;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #ecf0f1;
}
</style>
