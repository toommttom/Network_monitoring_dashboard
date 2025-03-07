<template>
  <div id="navbar">
    <nav class="vertical-navbar">
      <ul>
        <li>
          <router-link to="/" active-class="active">Home</router-link>
        </li>
        <li>
          <router-link to="/view" active-class="active">View</router-link>
        </li>
        <li>
          <router-link to="/map" active-class="active">Map</router-link>
        </li>
        <li>
          <router-link to="/alerte" active-class="active">Alerte</router-link>
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
  width: 10vw; /* Largeur ajustée à la hauteur de l'écran */
  background-color: #2c3e50;
  height: 100vh; /* Pleine hauteur */
  display: flex;
  flex-direction: column;
  padding-top: 2vh; /* Ajustement dynamique */
}

.vertical-navbar {
  width: 10vw;
  background-color: #2c3e50;
  color: white;
  padding: 2vh;
}

.vertical-navbar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.vertical-navbar li {
  margin: 2vh 0; /* Espacement dynamique */
}

.vertical-navbar a {
  color: white;
  text-decoration: none;
  font-size: 2.5vh; /* Taille de police relative à l'écran */
  transition: font-size 0.2s ease-in-out;
}

.vertical-navbar a.active {
  font-weight: bold;
  border-left: 0.5vh solid #3498db;
  padding-left: 1vh;
}

.content {
  flex: 1;
  padding: 2vh;
  background-color: #ecf0f1;
}
</style>
