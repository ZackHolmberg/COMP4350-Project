<template>
  <div id="wallet">
    <h1 id="walletAmount" class="wallet-header">{{ walletAmount }} BSC</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { mapState } from "vuex";

@Component({
  // Watches number of transactions
  computed: mapState(["transactions"]),

  // Checks if number of transactions has changed to determine if
  // new transaction was received
  created() {
    this.unwatch = this.$store.watch(
      (state: any, getters: { transactions: any }) => getters.transactions,
      (newValue: any, oldValue: any) => {
        if (newValue.length > oldValue.length) {
          this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
          const toSearch = []
          let i: number;
          for (i = oldValue.length; i < newValue.length; i++) {
            toSearch[toSearch.length] = newValue[i]
          }
          // Displays toast if transaction was recieved and the transaction is a non-send
          const temp = toSearch.find(
            (x) => x.type === "receive" || x.type === "reward"
          );
          if (temp) {
            console.log("New transaction received!");
            const message = "New transaction received!";
            this.$store.dispatch("ACTION_DISPLAY_TOAST", {
              message: message,
              type: "success",
            });
          }
        }
      }
    );
  },

  // Stops watching number of transactions
  beforeDestroy() {
    this.unwatch();
  },
})
export default class Wallet extends Vue {
  // Gets user wallet amount
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
