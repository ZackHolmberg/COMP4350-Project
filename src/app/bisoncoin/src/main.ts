import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue'
import store from './store'

Vue.use(VueRouter);

import HomePage from "./pages/HomePage.vue"
import LoginPage from "./pages/LoginPage.vue"


const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/', component: LoginPage },
    { path: '/home', component: HomePage },
  ]
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');