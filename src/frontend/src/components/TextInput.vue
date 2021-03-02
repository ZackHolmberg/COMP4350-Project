<template>
  <div>
    <input class="textInput" :placeholder="label" v-model="input"/>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class TextInput extends Vue {
  @Prop() private label!: string;

  data() {
    return {
      input: "",
    }
  }

// TODO: Grab user input and send it to the parent component
  inputData() {
    return this.$data.input;
  }

}
</script>

<style lang="scss">
@import "../style.scss";

.textInput {
  border-radius: $text-input-border-radius;
  box-shadow: $box-shadow;
  padding: 10px;
  border: border-color;
  margin: 25px;
  width: 30%;
  height: 35px;
  font-size: 16px;
  transition: $hover-transition;
  background-color: $text-input-background;
  color: $text-input-text;
}

.textInput:hover {
  cursor: pointer;
  transform: $hover-transform-text-input;
  box-shadow: $box-shadow-hover;
}
</style>
