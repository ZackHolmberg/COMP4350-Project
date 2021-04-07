<template>
  <div>
    <Button
      id="transaction-history-button"
      label="Transaction History"
      size="long"
      type="other"
      dest="/transactionHistory"
    />
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
  mounted() {
    this.$store.dispatch("ACTION_FETCH_TRANSACTION_HISTORY");
  }
}
</script>
