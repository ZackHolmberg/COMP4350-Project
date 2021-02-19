<template>
  <div>
    <router-link :to="dest" class="button" tag="button">{{
      label
    }}</router-link>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class Button extends Vue {
  @Prop() private label!: string;
  @Prop() private dest!: string;
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
  margin-top: 100px;
  margin-bottom: 50px;
  border: $border-color;
  color: $button-text;
}

.button:hover {
  cursor: pointer;
  transform: scale(1.25);
  box-shadow: $box-shadow-hover;
}
</style>
