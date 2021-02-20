<template>
  <div class="new-transaction">
    <p class="contact-text">Select Recipient: </p>
    <TextInput class="new-transaction-input" label="Contact" v-model="contact"/>
    <p class="amount-text">Amount: </p>
    <TextInput class="new-transaction-input" label="0.0 BSC" v-model="amount" />
    <CancelButton class="transaction-cancel-button" dest="/home" label="Cancel" />
    <Button class="send-button" dest="/home" label="Send" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TextInput from "../components/TextInput.vue";
import Button from "../components/Button.vue";
import CancelButton from "../components/CancelButton.vue";

@Component({
  methods: {
    newTransaction(transactionAmount, contactName) {
        //this.$store.dispatch("sendTransaction");
    }
  },

  components: {
    TextInput,
    Button,
    CancelButton,
  },

  data: function() {
      return {
        amount: "",
        contact: ""
      }
  },
})
export default class NewTransactionPage extends Vue {
}
</script>

<style lang="scss">
@import "../style.scss";

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
  right: 450px;
  padding: 10px;
}

.transaction-cancel-button {
  position: absolute;
  left: 450px;
  padding: 10px;
}

.amount-text {
  position: absolute;
  left: 340px;
  padding-top: 20px;
  margin-right: 5px;
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.contact-text {
  position: absolute;
  left: 265px;
  padding-top: 20px;
  margin-right: 5px;
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.new-transaction-input {
  position: relative;
  left: 0px;
}
</style>