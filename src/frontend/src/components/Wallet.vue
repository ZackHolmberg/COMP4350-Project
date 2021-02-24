<template>
  <div class="container">
    <h1>{{ walletAmount }} BSC</h1>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  computed: {
    walletAmount() {
      return this.$store.state.walletAmount;
    },
    walletId() {
      return this.$store.state.walletId;
    },
    privateKey() {
      return this.$store.state.privateKey;
    },
  },
  beforeMount() {
    console.log("hi");
    this.$store.dispatch("fetchWalletAmount");
  },
})
export default class Wallet extends Vue {
  @Prop() private label!: string;
}
</script>

<style lang="scss">
@import "../style.scss";

.container {
  width: 40%;
  height: 40%;
  //   padding: 10px;
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
