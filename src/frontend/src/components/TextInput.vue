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
  @Prop() private label!: string;
  @Prop() private disable!: boolean;
  @Prop() private type!: string;
  @Prop({ default: false }) private edit!: boolean;

  data() {
    return {
      input: "",
    };
  }

  getClass() {
    if(!this.edit) {
      return "text-input";
    } else {
      return "text-input-edit";
    }
  }

  inputData() {
    return this.$data.input;
  }
}
</script>

<style lang="scss">
@import "../style.scss";

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
  background-color: $text-input-background;
  color: $text-input-color;
}

.text-input:hover {
  cursor: pointer;
  transform: $hover-transform-text-input;
  box-shadow: $box-shadow-hover;
}

.text-input-edit {
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
  background-color: $text-input-edit-background;
  color: $text-input-edit-color;
}

.text-input-edit::placeholder {
  color: $text-input-edit-color;
}

.text-input-edit:hover {
  cursor: pointer;
  transform: $hover-transform-text-input;
  box-shadow: $box-shadow-hover;
}
</style>
