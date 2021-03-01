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
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  padding: 1%;
  background-color: gray;
  text-align: center;
  box-shadow: $box-shadow;
  border-radius: 10px;
  display: inline-block;
  width: 55%;
  height: 67.5%;
  border: $border-color;
}

.wallet-component {
  position: absolute;
}

.transaction-component {
  position: relative;
  margin-top: 30%;
}
</style>
