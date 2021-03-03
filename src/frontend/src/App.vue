<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script lang="ts">
import { Vue } from "vue-property-decorator";

export default class App extends Vue {}
</script>

<style lang="scss">
@import "./style.scss";

body {
  background-color: $background-color;
  margin: 0px;
  padding: 0px;
}
</style>