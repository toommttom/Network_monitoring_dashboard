import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import AddTableauPage from "./views/AddTableauPage.vue";
import EditTableau from "./components/EditTableau.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/addtableaux",
      name: "add",
      component: AddTableauPage,
    },
    {
      path: "/modifier_tableau/:id",
      name: "edit",
      component: EditTableau,
    },
  ],
});
