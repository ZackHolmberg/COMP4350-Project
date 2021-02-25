<template>
  <div>
    <router-link :to="dest" class="big-button" tag="button">{{
      label
    }}</router-link>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class BigButton extends Vue {
  @Prop() private label!: string;
  @Prop() private dest!: string;
}
</script>

<style lang="scss">
@import "../style.scss";

.big-button {
  background-color: $big-button-background-color;
  width: 300px;
  height: 100px;
  border-radius: 40px;
  box-shadow: $box-shadow;
  font-size: 32px;
  transition: 0.2s linear;
  border: $border-color;
  color: $button-text;
  margin-top: 75px;
  margin-bottom: 50px;
}

.big-button:hover {
  cursor: pointer;
  transform: scale(1.25);
  box-shadow: $box-shadow-hover;
}
</style>
