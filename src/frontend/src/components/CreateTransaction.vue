<template>
  <div class="create-transaction">
    <BigButton id="transaction-button" dest="/transaction" label="New Transaction" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import BigButton from "../components/BigButton.vue";

@Component({
  components: {
    BigButton,
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
