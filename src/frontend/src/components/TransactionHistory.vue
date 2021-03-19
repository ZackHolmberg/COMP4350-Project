<template>
  <div class="transaction-history">
      <div v-for="item in transactions" :key="item.transaction.id">
        <p v-if="item.type == 'receive'" 
          class="received"> 
          Date: {{ item.transaction.date }} From: {{ item.transaction.from }} Amount: {{ item.transaction.amount }} BSC 
        </p>
        <p v-else-if="item.type == 'send'"  
          class="sent"> 
          Date: {{ item.transaction.date }} To: {{ item.transaction.to }} Amount: {{ item.transaction.amount }} BSC
        </p>
         <p v-else-if="item.type == 'reward'"  
          class="reward"> 
          Date: {{ item.transaction.date }} From: {{ item.transaction.from }} Amount: {{ item.transaction.amount }} BSC
        </p>
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class TransactionHistory extends Vue {  
  data() {
    return {
      transactions: [
        {
          transaction: {
            id: 1,
            date: "Thursday, March 11th",
            from: "fromPerson",
            amount: 10
          },
          type: "receive"
        },
        {
          transaction: {
            id: 2,
            date: "Thursday, March 10th",
            to: "toPerson",
            amount: 200
          },
          type: "send"
        },
        {
          transaction: {
            id: 3,
            date: "Thursday, March 9th",
            from: "fromPerson",
            amount: 5
          },
          type: "reward"
        }
      ],
    }
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.received {
  background-color: lightgreen;
  color: black;
}

.sent {
  background-color: lightsalmon;
  color: black;
}

.reward {
  background-color: lightblue;
  color: black;
}

.transaction-history {
  background-color: lightgray;
}

.header {
  font-size: 20px;
  font-weight: bold;
  color: black;
}
</style>