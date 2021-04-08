<template>
  <div class="list-row">
    <div class="row-text">
      <p class="address-text">
        <!-- If the transaction type is a send, display the transaction's "to_address". Otherwise, 
        for the receive and reward types, displayt the transaction's "from_address" -->
        {{
          this.type == "send"
            ? this.transaction.to_address
            : this.transaction.from_address
        }}
      </p>
      <p class="type-text">
        <!-- Display the transaction type corresponding to the type prop -->
        {{
          this.type == "send"
            ? "Sent"
            : this.type == "receive"
            ? "Received"
            : "Reward"
        }}
        <!-- Display the transaction's time in UNIX format as something more human-readable -->
        {{ " | " + convertDate(this.transaction.timestamp) }}
      </p>
    </div>
    <div v-bind:class="getClass()">
      <!-- Display the transaction's amount. If the transaction is a send, represent the amount as a negative. -->
      {{ this.type == "send" ? "-" : "" }}{{ this.transaction.amount }} BSC
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import type { Transaction } from "../types";

@Component
// ListItem repesents a single item in the transaction history list. It displays information about a transaction.
export default class ListItem extends Vue {
  @Prop() private transaction!: Transaction;
  @Prop() private type!: string;

  // Returns the proper class of the component based on the transaction's type
  getClass() {
    return `row-amount ${this.type}`
  }

  // Converts the UNIX formatted timestamp into a human-readable format
  convertDate(time: number) {
    const d = new Date(0);
    d.setUTCSeconds(time);
    return d.toDateString();
  }

}
</script>

<style lang="scss">
@import "../style.scss";
.list-row {
  background-color: $list-row-background-color;
  overflow: hidden;
  padding: $list-row-padding;
  color: $list-row-color;
  box-shadow: $box-shadow-hover;
  border-bottom: $list-row-border-bottom;
}

.row-text {
  float: left;
  text-align: left;
}

.row-amount {
  text-align: right;
  margin-top: $row-amount-margin-top;
  font-weight: bolder;
  font-size: $address-text-font-size;
  border-radius: $row-amount-border-radius;
  float: right;
  padding: $row-amount-padding;
}

.address-text {
  font-weight: bolder;
  font-size: $address-text-font-size;
}

.type-text {
  font-weight: $type-text-font-weight;
  font-size: $type-text-font-size;
}

.receive {
  background-color: $receive-background-color;
  color: $receive-color;
}

.send {
  background-color: $send-background-color;
  color: $send-color;
}

.reward {
  background-color: $reward-background-color;
  color: $reward-color;
}
</style>
