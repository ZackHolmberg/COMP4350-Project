<template>
  <div>
    <input
      :class='getClass()'
      :placeholder="label"
      v-model="input"
      :disabled="disable"
      :type="type"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class TextInput extends Vue {
  // Placeholder label on input
  @Prop() private label!: string;

  // If input should be disabled
  @Prop() private disable!: boolean;

  // Type of input
  @Prop() private type!: string;

  // If input is in edit mode
  @Prop({ default: false }) private edit!: boolean;

  data() {
    return {
      // User input
      input: "",
    };
  }

  // Determines class of text input based on prop
  getClass() {
    if(!this.edit) {
      return "text-input default-input";
    } else {
      return "text-input edit-input";
    }
  }

  // Returns user input
  inputData() {
    return this.$data.input;
  }
}
</script>

<style lang="scss">
@import "../style.scss";

// COLOUR
.default-input {
  background-color: $text-input-background;
  color: $text-input-color;
}

.edit-input {
  background-color: $text-input-edit-background;
  color: $text-input-edit-color;
}

.edit-input::placeholder {
  color: $text-input-edit-color;
}
// END -- COLOUR

.text-input {
  border-radius: $text-input-border-radius;
  box-shadow: $box-shadow;
  padding: $text-input-padding;
  border: $border-color;
  margin: $text-input-margin;
  width: $text-input-width;
  height: $text-input-height;
  font-size: $text-input-font-size;
  font-family: $default-font;
  transition: $hover-transition;
}

.text-input:hover {
  cursor: pointer;
  transform: $hover-transform-text-input;
  box-shadow: $box-shadow-hover;
}
</style>
