<template>
  <div class="home">
    <div class="bison">BisonCoin</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class HomePage extends Vue {}
</script>

<style>
.bison {
  margin: 40px 0px;
  color: gray;
}
</style>
