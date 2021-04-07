<template>
  <div class="list-row">
    <div class="row-text">
      <p class="address-text">
        {{
          this.type == "send"
            ? this.transaction.to_address
            : this.transaction.from_address
        }}
      </p>
      <p class="type-text">
        {{
          this.type == "send"
            ? "Sent"
            : this.type == "receive"
            ? "Received"
            : "Reward"
        }}
        {{ " | " + convertDate(this.transaction.timestamp) }}
      </p>
    </div>
    <div v-bind:class="getClass()">
      {{ this.type == "send" ? "-" : "" }}{{ this.transaction.amount }} BSC
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import type { Transaction } from "../types";

@Component
export default class ListItem extends Vue {
  @Prop() private transaction!: Transaction;
  @Prop() private type!: string;

  getClass() {
    return `row-amount ${this.type}`
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
