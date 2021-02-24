<template>
  <div>
    <router-link :to="dest" class="button" tag="button" @click.native="handleClick">{{
      label
    }}</router-link>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Emit } from "vue-property-decorator";

@Component
export default class Button extends Vue {
  @Prop() private label!: string;
  @Prop() private dest!: string;
  

  /* data() {
    return {
      amount: "59",
      contact: "Me"
    }
  } */

  handleClick() {
    this.$emit('send');
    console.log("clicked");

    //const values = { amount: this.$data.amount, contact: this.$data.contact};
    //this.$store.dispatch("sendTransaction", values);
  }

}
</script>

<style lang="scss">
@import "../style.scss";

.button {
  background-color: $button-background-color;
  width: 100px;
  height: 50px;
  border-radius: 25px;
  box-shadow: $box-shadow;
  font-size: 16px;
  transition: 0.2s linear;
  border: $border-color;
  color: $button-text;
}

.button:hover {
  cursor: pointer;
  transform: scale(1.25);
  box-shadow: $box-shadow-hover;
}
</style>
