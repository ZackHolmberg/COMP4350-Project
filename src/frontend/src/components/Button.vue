<template>
  <div>
    <router-link v-if="size == 'big' && type == 'default'" :to="dest" class="big-button default" tag="button">{{
      label
    }}</router-link>
    <router-link v-else-if="size == 'small' && type == 'default'" :to="dest" class="button default" tag="button">{{
      label
    }}</router-link>
    <router-link v-if="size == 'big' && type == 'cancel'" :to="dest" class="big-button cancel" tag="button">{{
      label
    }}</router-link>
    <router-link v-else-if="size == 'small' && type == 'cancel'" :to="dest" class="button cancel" tag="button">{{
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
  @Prop() private size!: string;
  @Prop() private type!: string;
}
</script>

<style lang="scss">
@import "../style.scss";
.cancel {
  background-color: $cancel-button-background-color;
}

.default {
  background-color: $button-background-color;
}

.big-button {
  width: $big-button-width;
  height: $big-button-height;
  border-radius: $big-button-border-radius;
  box-shadow: $box-shadow;
  font-size: $big-button-font-size;
  transition: $hover-transition;
  border: $border-color;
  color: $button-text;
}

.button {
  width: $button-width;
  height: $button-height;
  border-radius: $button-border-radius;
  box-shadow: $box-shadow;
  font-size: $button-font-size;
  transition: $hover-transition;
  border: $border-color;
  color: $button-text;
}

.button:hover {
  cursor: pointer;
  transform: $hover-transform-button;
  box-shadow: $box-shadow-hover;
}

.big-button:hover {
  cursor: pointer;
  transform: $hover-transform-button;
  box-shadow: $box-shadow-hover;
}
</style>
