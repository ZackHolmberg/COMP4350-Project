import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue'
import store from './store'
import HomePage from "./pages/HomePage.vue"
import LoginPage from "./pages/LoginPage.vue"
import NewTransactionPage from "./pages/NewTransactionPage.vue"
import ViewAccountPage from "./pages/ViewAccountPage.vue"
import CreateAccountPage from "./pages/CreateAccountPage.vue";

Vue.use(VueRouter);

export const router = new VueRouter({
  mode: "history",
  routes: [
    { path: "/", component: LoginPage },
    { path: "/home", component: HomePage },
    { path: "/transaction", component: NewTransactionPage },
    { path: "/createAccount", component: CreateAccountPage },
    { path: '/account', component: ViewAccountPage},
  ],
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
