<template>
  <div class="home">
    <div class="wrapper"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class HomePage extends Vue {}
</script>

<style lang="scss">
@import "../style.scss";
.wrapper {
  margin: 10%;
  padding: 10%;
  background-color: $background-color;
}
</style>
