<template>
<div>
  <NavBar />
  <div class="wrapper">
    <Wallet class="wallet-component"/>
    <CreateTransaction class="transaction-component"/>
  </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Wallet from "../components/Wallet.vue";
import CreateTransaction from "../components/CreateTransaction.vue";
import NavBar from "../components/NavBar.vue";

@Component({
  components: {
    Wallet,
    CreateTransaction,
    NavBar,
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
  box-shadow: $box-shadow;
  border-radius: $box-border-radius;
  width: $home-page-wrapper-size;
  min-width: $home-page-wrapper-min-size;
  height: $home-page-wrapper-size;
  min-height: $home-page-wrapper-min-size;
  border: $border-color;
}

.wallet-component {
  position: relative;
}

.transaction-component {
  position: relative;
  bottom: $home-page-transaction-bottom;
}
</style>
