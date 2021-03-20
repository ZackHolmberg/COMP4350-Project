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
        <div v-for="item in transactions" :key="item.transaction.id">
          <p v-if="item.type == 'receive'" class="received content-text"> 
            Date: {{ item.transaction.date }} From: {{ item.transaction.from }} Amount: {{ item.transaction.amount }} BSC 
          </p>
          <p v-else-if="item.type == 'send'" class="sent content-text"> 
            Date: {{ item.transaction.date }} To: {{ item.transaction.to }} Amount: {{ item.transaction.amount }} BSC
          </p>
          <p v-else-if="item.type == 'reward'" class="reward content-text"> 
            Date: {{ item.transaction.date }} From: {{ item.transaction.from }} Amount: {{ item.transaction.amount }} BSC
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

  collapse() {
    if(this.$data.active) {
      this.$data.active = false;
    }
    else {
      this.$data.active = true;
    }  
  }

  mounted() {
    this.$store.dispatch("ACTION_GET_TRANSACTION_HISTORY");
  }

  get transactions() {
    return this.$store.getters.transactions;
  }
}
</script>

<style lang="scss">
@import "../style.scss";
.content {
  text-align: center;
  overflow: hidden;
  padding: 18px;
  display: 'none';
  background-color: lightgrey;
  font-size: 18px;
}

.received {
  background-color: lightgreen;
}

.sent {
  background-color: lightsalmon;
}

.reward {
  background-color: lightblue;
}

.content-text {
  color: black;
  padding: 5px;
  margin: auto;
}
</style>
