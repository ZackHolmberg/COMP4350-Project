<template>
  <div class="wrapper">
    <Wallet />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Wallet from "../components/Wallet.vue";

@Component({
  components: {
    Wallet,
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
  // float: left;
  display: inline-block;
  width: 55%;
  height: 67.5%;
  border: $border-color;
}
</style>
