<template>
  <div>
    <Button
      id="transaction-history-button"
      label="Transaction History"
      size="long"
      type="other"
      @click.native="collapse"
    />
    <div v-if="active" id="content" class="content">
      <p v-if="transactions.length == 0" class="no-transaction-history">
        No Transaction History
      </p>
      <div v-for="item in transactions" :key="item.transaction.id">
        <p v-if="item.type == 'receive'" class="received content-text">
          DATE: {{ convertDate(item.transaction.timestamp) }}, FROM:
          {{ item.transaction.from_address }}, AMOUNT:
          {{ item.transaction.amount }} BSC
        </p>
        <p v-else-if="item.type == 'send'" class="sent content-text">
          DATE: {{ convertDate(item.transaction.timestamp) }}, TO:
          {{ item.transaction.to_address }}, AMOUNT:
          {{ item.transaction.amount }} BSC
        </p>
        <p v-else-if="item.type == 'reward'" class="reward content-text">
          DATE: {{ convertDate(item.transaction.timestamp) }}, FROM:
          {{ item.transaction.from_address }}, AMOUNT:
          {{ item.transaction.amount }} BSC
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Button from "./Button.vue";

@Component({
  components: {
    Button,
  },
})
export default class TransactionHistory extends Vue {
  data() {
    return {
      active: false,
    };
  }

  mounted() {
    this.$store.dispatch("ACTION_FETCH_TRANSACTION_HISTORY");
  }

  get transactions() {
    return this.$store.getters.transactions;
  }

  collapse() {
    this.$data.active = !this.$data.active;
  }

  convertDate(time: number) {
    const d = new Date(0);
    d.setUTCSeconds(time);
    return d.toDateString();
  }
}
</script>

<style lang="scss">
@import "../style.scss";
.content {
  text-align: left;
  padding: $content-padding;
  background-color: $content-background-color;
  font-size: $content-font-size;
  color: black;
  border-radius: $content-border-radius;
  border: $border-color;
  box-shadow: $box-shadow;
}

.received {
  background-color: $received-color;
}

.sent {
  background-color: $sent-color;
}

.reward {
  background-color: $reward-color;
}

.no-transaction-history {
  font-weight: bold;
  color: $no-transactions-text-color;
  text-align: center;
}

.content-text {
  padding: $content-text-padding;
  margin: $content-text-margin;
  border: $home-page-border;
}
</style>
