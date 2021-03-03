<template>
  <div id="wallet" class="wallet">
    <h1>{{ walletAmount }} BSC</h1>
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

  // Is this better in the component or in @Component, under methods?
  beforeMount() {
      this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.wallet {
  width: 60%;
  height: 60%;
  text-align: center;
  border-radius: 10px;
  display: inline-block;
  margin: 25px;
}

h1 {
  font-size: 150px;
  color: white;
}
</style>
