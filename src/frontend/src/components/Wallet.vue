<template>
  <div id="wallet">
    <h1 id="walletAmount" class="wallet-header">{{ walletAmount }} BSC</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Wallet extends Vue {
  get walletAmount() {
    return this.$store.getters.walletAmount;
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.wallet-header {
  font-size: $wallet-font-size;
  color: $default-text-color;
}
</style>
