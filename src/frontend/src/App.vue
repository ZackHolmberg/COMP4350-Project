<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script lang="ts">
import { Vue } from "vue-property-decorator";

export default class App extends Vue {}
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;400&display=swap");
body {
  font-family: "Montserrat", sans-serif;
}
</style>
