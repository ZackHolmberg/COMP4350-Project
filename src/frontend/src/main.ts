import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue'
import store from './store'
import HomePage from "./pages/HomePage.vue"
import LoginPage from "./pages/LoginPage.vue"
import NewTransactionPage from "./pages/NewTransactionPage.vue"

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/', component: LoginPage },
    { path: '/home', component: HomePage },
    { path: '/transaction', component: NewTransactionPage},
  ]
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');