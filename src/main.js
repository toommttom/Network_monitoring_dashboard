import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/HomePage.vue";

// Définir les routes
const routes = [{ path: "/", component: Home }];

// Créer le routeur
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Créer l'application Vue et lier le routeur
createApp(App).use(router).mount("#app");
