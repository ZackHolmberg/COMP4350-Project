<template>
  <div class="create-transaction">
    <Button 
      id="transaction-button" 
      dest="/transaction" 
      label="New Transaction" 
      :big="true"
      :cancel="false"
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

<style lang="scss">
@import "../style.scss";

.create-transaction {
  width: 60%;
  height: 60%;
  text-align: center;
  border-radius: 10px;
  display: inline-block;
  margin: 25px;
}
</style>
