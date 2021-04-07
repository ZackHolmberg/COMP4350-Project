<template>
  <div>
    <h1 class="transaction-history-header">Transaction History</h1>

    <div id="content" class="content">
      <p v-if="transactions.length == 0" class="no-transaction-history">
        No Transaction History
      </p>
      <div v-for="item in transactions" :key="item.transaction.id">
        <ListItem :type="item.type" :transaction="item.transaction" />
      </div>
    </div>
    <Button
      id="transaction-history-back-button"
      class="transaction-history-back-button"
      label="Back"
      size="small"
      type="default"
      dest="/home"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ListItem from "../components/ListItem.vue";
import Button from "../components/Button.vue";

@Component({
  components: {
    ListItem,
    Button,
  },
})
export default class TransactionHistoryPage extends Vue {
  get transactions() {
    return this.$store.getters.transactions;
  }
}
</script>

<style lang="scss">
@import "../style.scss";
.content {
  top: $transaction-wrapper-top;
  left: 0;
  right: 0;
  margin: auto;
  padding: $content-padding;
  text-align: center;
  width: $transaction-wrapper-width;
  height: $content-height;
  overflow: auto;
  border-radius: $content-border-radius;
  box-shadow: $box-shadow-hover;
  background-color: $content-background-color;
}

.no-transaction-history {
  font-weight: bold;
  color: $no-transactions-text-color;
  text-align: center;
}

.transaction-history-header {
  font-size: $default-header-font-size;
  text-align: center;
  font-weight: bold;
  color: $default-text-color;
}

.transaction-history-back-button {
  margin-top: $transaction-history-back-button-margin-top;
  text-align: center;
}
</style>
