<template>
  <div class="new-transaction">
    <div class="transaction-wrapper">
      <p class="transaction-text">Recipient:</p>
      <TextInput
        id="contact-input"
        class="new-transaction-input"
        label="UMNetID"
        ref="recipient"
        :disable="false"
      />
      <p class="transaction-text">Amount:</p>
      <TextInput
        id="amount-input"
        class="new-transaction-input"
        label="0.0 BSC"
        ref="amount"
        :disable="false"
      />
      <Button
        id="transaction-cancel"
        class="transaction-cancel-button"
        dest="/home"
        label="Cancel"
        size="small"
        type="cancel"
      />
      <Button
        id="transaction-send"
        class="transaction-send-button"
        dest=""
        label="Send"
        size="small"
        type="default"
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
// NewTransactionPage is where users enter the UMNetID of their intended recipient and an amount to send in order to create a new transaction
export default class NewTransactionPage extends Vue {
  // Grabs the input entered into the two text inputs on the page and dispatches the send transaction action with the data passed as an object
  newTransaction() {
    const recipient = this.$refs.recipient.inputData();
    const amount = this.$refs.amount.inputData();
    const values = {
      amount: amount,
      recipient: recipient,
    };
    this.$store.dispatch("ACTION_SEND_TRANSACTION", values);
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.transaction-wrapper {
  position: absolute;
  top: $transaction-wrapper-top;
  left: 0;
  right: 0;
  margin: auto;
  padding: 1%;
  text-align: center;
  width: $transaction-wrapper-width;
}

.new-transaction {
  -webkit-font-smoothing: antialiased;
}

.transaction-send-button {
  position: absolute;
  left: $transaction-button-position;
  padding: $transaction-button-padding;
}

.transaction-cancel-button {
  position: absolute;
  right: $transaction-button-position;
  padding: $transaction-button-padding;
}

.transaction-text {
  position: absolute;
  left: $transaction-text-left;
  padding-top: $transaction-text-padding-top;
  font-size: $transaction-text-font-size;
  font-weight: bold;
  color: $default-text-color;
}

.new-transaction-input {
  position: relative;
  width: $transaction-input-width;
  right: $transaction-input-right;
}
</style>
