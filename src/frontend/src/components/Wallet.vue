<template>
  <div class="container">
    <h1>{{ walletAmount }} BSC</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Wallet extends Vue {
  get walletAmount() {
    return this.$store.state.walletAmount;
  }

  walletId() {
    return this.$store.state.walletId;
  }

  privateKey() {
    return this.$store.state.privateKey;
  }

  walletCreated() {
    return this.$store.state.walletCreated;
  }

  beforeMount() {
    if (this.walletCreated()) {
      this.$store.dispatch("fetchWalletAmount");
    } else {
      this.$store.dispatch("initializeWallet");
      this.$store.dispatch("fetchWalletAmount");
    }
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.container {
  width: 40%;
  height: 40%;
  background-color: lightgray;
  text-align: center;
  box-shadow: $box-shadow-hover;
  border-radius: 10px;
  display: inline-block;
  margin: 25px;
  border: $border-color;
}

h1 {
  padding: 25%;
}
</style>
