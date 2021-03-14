<template>
  <div class="new-transaction">
    <div class="transaction-wrapper">
      <p class="transaction-text">Recipient:</p>
      <TextInput
        id="contact-input"
        class="new-transaction-input"
        label="Email"
        :disable="false"
      />
      <p class="transaction-text">Amount:</p>
      <TextInput
        id="amount-input"
        class="new-transaction-input"
        label="0.0 BSC"
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
        dest="/home"
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
export default class NewTransactionPage extends Vue {
  newTransaction() {
    const values = {
      amount: 1,
      contact:
        "-----BEGIN PUBLIC KEY-----\r\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCSg2uhKFfV8nhIGqtueVZr0HXR\r\nUPM9XbjRf85854ZUBkKfw1mLo+uMXn37W/51jtDaLxa1gvQDeOZhDjo26aCHir4l\r\n9Io2iIoNDuS3nuQI9NJEJIMD9OSfFSccC0tD4JEFqDn73UN6rID72i3WGUn2A+Bn\r\nAktbWrx0p989PJgwmQIDAQAB\r\n-----END PUBLIC KEY-----\r\n",
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
