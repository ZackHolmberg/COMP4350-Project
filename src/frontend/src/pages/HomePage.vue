<template>
<div>
  <NavBar />
  <div class="wrapper">
    <Wallet class="wallet-component"/>
    <CreateTransaction class="transaction-component"/>
    <Mining class="mining-component"/>
    <TransactionHistory class="transaction-history-component"/>
  </div>
</div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Wallet from "../components/Wallet.vue";
import CreateTransaction from "../components/CreateTransaction.vue";
import NavBar from "../components/NavBar.vue";
import Mining from "../components/Mining.vue";
import TransactionHistory from "../components/TransactionHistory.vue";

@Component({
  components: {
    Wallet,
    CreateTransaction,
    NavBar,
    Mining,
    TransactionHistory,
  },
})
export default class HomePage extends Vue {}
</script>

<style lang="scss">
@import "../style.scss";
.wrapper {
  position: absolute;
  top: $home-page-wrapper-top;
  left: 0px;
  right: 0px;
  margin-left: auto;
  margin-right: auto;
  background-color: $home-page-background-color;
  text-align: center;
  box-shadow: $box-shadow-hover;
  border-radius: $box-border-radius;
  width: $home-page-wrapper-size;
  min-width: $home-page-wrapper-min-width;
  max-width: $home-page-wrapper-max-width;
  height: $home-page-wrapper-size;
  min-height: $home-page-wrapper-min-height;
  //max-height: $home-page-wrapper-max-height;
  border: $home-page-border;
}

.wallet-component {
  position: absolute;
  width: 100%;
  bottom: 45%;
}

.transaction-component {
  position: absolute;
  bottom: $home-page-button-bottom;
  left: $home-page-button-position;
}

.mining-component {
  position: absolute;
  bottom: $home-page-button-bottom;
  right: $home-page-button-position;
}

.transaction-history-component {
  position: absolute;
  width: 100%;
  bottom: 10%;
}
</style>
