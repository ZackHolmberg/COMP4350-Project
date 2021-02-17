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
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  font-size: 16px;
  transition: 0.2s linear;
  margin-top: 100px;
  margin-bottom: 50px;
  border: 1px solid $border-color;
  color: $button-text;
}

.button:hover {
  cursor: pointer;
  transform: scale(1.25);
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}
</style>
