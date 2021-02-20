<template>
  <div class="create-transaction">
    <BigButton dest="/transaction" label="New Transaction" />
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
  width: 40%;
  height: 40%;
  background-color: lightgray;
  text-align: center;
  box-shadow: $box-shadow-hover;
  border-radius: 10px;
  display: inline-block;
  margin: 25px;
  border: $border-color;
}
</style>
