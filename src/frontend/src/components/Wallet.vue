<template>
  <div id="wallet" class="wallet">
    <h1 class="wallet-header">{{ walletAmount }} BSC</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Wallet extends Vue {
  get walletAmount() {
    return this.$store.getters.walletAmount;
  }

  // TODO: Remove this function once we initialize wallet on account creation
  walletCreated() {
    return this.$store.getters.walletCreated;
  }

  beforeMount() {
    // TODO: Remove this conditional once we initialize wallet on account creation and only fetch wallet amount
    if (this.walletCreated()) {
      this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
    } else {
      this.$store.dispatch("ACTION_INITIALIZE_WALLET");
      this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
    }
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.wallet-header {
  font-size: 150px;
  color: white;
}
</style>
