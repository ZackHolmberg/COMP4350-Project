<template>
  <div>
    <Button 
      id="transaction-history-button" 
      dest="" 
      label="Transaction History" 
      size="long"
      type="other"
      @click.native="collapse"
    />
      <!------- OPENS COLLAPSIBLE ------->
      <div v-if="active" class="content">
        <p v-if="transactions.length == 0" class="no-transaction-history"> No Transaction History. </p>
        <div v-for="item in transactions" :key="item.transaction.id">
          <p v-if="item.type == 'receive'" class="received content-text"> 
            Date: {{ item.transaction.date }}, From: {{ item.transaction.from }}, Amount: {{ item.transaction.amount }} BSC 
          </p>
          <p v-else-if="item.type == 'send'" class="sent content-text"> 
            Date: {{ item.transaction.date }}, To: {{ item.transaction.to }}, Amount: {{ item.transaction.amount }} BSC
          </p>
          <p v-else-if="item.type == 'reward'" class="reward content-text"> 
            Date: {{ item.transaction.date }}, From: {{ item.transaction.from }}, Amount: {{ item.transaction.amount }} BSC
          </p>
        </div>
      </div>
      <!------- END -- OPENS COLLAPSIBLE ------->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Button from "./Button.vue";

@Component({
  components: {
    Button
  },
})
export default class TransactionHistory extends Vue {
  data() {
    return {
      active: false,
    }
  }

  mounted() {
    this.$store.dispatch("ACTION_GET_TRANSACTION_HISTORY");
  }

  get transactions() {
    return this.$store.getters.transactions;
  }

  collapse() {
    if(this.$data.active) {
      this.$data.active = false;
    }
    else {
      this.$data.active = true;
    }  
  }
}
</script>

<style lang="scss">
@import "../style.scss";
.content {
  text-align: center;
  padding: $content-padding;
  background-color: $content-background-color;
  font-size: $content-font-size;
  color: $default-text-color;
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
}

.content-text {
  padding: $content-text-padding;
  margin: auto;
}
</style>
