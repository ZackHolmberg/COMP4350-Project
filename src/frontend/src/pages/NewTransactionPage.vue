<template>
  <div class="new-transaction">
    <div class="transaction-wrapper">
      <p class="contact-text">Recipient: </p>
      <TextInput id=contact-input class="new-transaction-input" label="Email"/>
      <p class="amount-text">Amount: </p>
      <TextInput id=amount-input class="new-transaction-input" label="0.0 BSC"/>
      <Button 
        id=transaction-cancel 
        class="transaction-cancel-button" dest="/home" 
        label="Cancel" 
        :big="false" 
        :cancel="true"
      />
      <Button 
        id=transaction-send 
        class="send-button" 
        dest="/home" 
        label="Send" 
        :big="false"
        :cancel="false"
        @click.native="newTransaction" 
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TextInput from "../components/TextInput.vue";
import Button from "../components/Button.vue";

@Component({
  components: {
    TextInput,
    Button,
  },
})
export default class NewTransactionPage extends Vue {
  newTransaction() {
     const values = { amount: 10, contact: "email"};
     this.$store.dispatch("ACTION_SEND_TRANSACTION", values);
  }  
}
</script>

<style lang="scss">
@import "../style.scss";

.transaction-wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  padding: 1%;
  text-align: center;
  border-radius: 10px;
  display: inline-block;
  width: 600px;
  height: 67.5%;
}

.new-transaction {
  margin-top: 100px;
  text-align: center;
  padding: 2px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: $background-color;
}

.send-button {
  position: absolute;
  left: 20%;
  padding: 10px;
}

.transaction-cancel-button {
  position: absolute;
  right: 20%;
  padding: 10px;
}

.amount-text {
  position: absolute;
  left: 80px;
  padding-top: 20px;
  margin-right: 5px;
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.contact-text {
  position: absolute;
  left: 80px;
  padding-top: 20px;
  margin-right: 5px;
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.new-transaction-input {
  position: relative;
  width: 1000px;
  right: 150px;
}
</style>