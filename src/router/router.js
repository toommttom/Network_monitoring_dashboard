import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import MapPage from "../views/MapPage.vue";
import PrediPage from "@/views/PrediPage.vue";
import ViewPage from "@/views/ViewPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/map",
    name: "map",
    component: MapPage,
  },
  {
    path: "/predi",
    name: "predi",
    component: PrediPage,
  },
  {
    path: "/view",
    name: "view",
    component: ViewPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Utiliser l'historique HTML5
  routes, // Définir les routes
});

export default router;
