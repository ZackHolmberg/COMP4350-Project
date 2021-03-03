<template>
  <div>
    <input class="textInput" :placeholder="label" v-model="input" :disabled="disabled"/>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class TextInput extends Vue {
  @Prop() private label!: string;
  @Prop() private disabled!: string;

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
  border-radius: 25px;
  box-shadow: $box-shadow;
  padding: 10px;
  border: border-color;
  margin: 25px;
  width: 30%;
  height: 35px;
  font-size: 16px;
  transition: 0.2s linear;
  background-color: $text-input-background;
  color: $text-input-text;
}

.textInput:hover {
  cursor: pointer;
  transform: scale(1.05);
  box-shadow: $box-shadow-hover;
}
</style>
