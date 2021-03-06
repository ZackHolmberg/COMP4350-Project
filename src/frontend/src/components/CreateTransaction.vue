<template>
  <div>
    <Button 
      id="transaction-button" 
      dest="/transaction" 
      label="New Transaction" 
      size="big"
      type="default"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Button from "../components/Button.vue";

@Component({
  components: {
    Button,
  },
})
export default class CreateTransaction extends Vue {}
</script>
