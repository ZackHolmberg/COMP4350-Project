<template>
  <div class="home">
    <div class="wrapper">
      <CreateTransaction />
      <CreateTransaction />
      <CreateTransaction />
      <CreateTransaction />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import CreateTransaction from "../components/CreateTransaction.vue";

@Component({
  components: {
    CreateTransaction,
  },
})
export default class HomePage extends Vue {}
</script>

<style lang="scss">
@import "../style.scss";
.wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  padding: 1%;
  background-color: gray;
  text-align: center;
  box-shadow: $box-shadow;
  border-radius: 10px;
  display: inline-block;
  width: 55%;
  height: 67.5%;
  border: $border-color;
}
</style>
