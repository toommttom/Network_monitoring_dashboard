import { createApp } from "vue";
import App from "./App.vue";
// import { createRouter, createWebHistory } from "vue-router";
// import Home from "./views/HomePage.vue";
import router from "./router/router.js";

// Créer l'application Vue et lier le routeur
createApp(App).use(router).mount("#app");
