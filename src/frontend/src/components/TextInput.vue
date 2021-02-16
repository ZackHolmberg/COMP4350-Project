<template>
  <div>
    <input class="textInput" :placeholder="label" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class TextInput extends Vue {
  @Prop() private label!: string;
}
</script>

<style>
.textInput {
  border-radius: 25px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  padding: 10px;
  border: 1px solid black;
  margin: 25px;
  width: 30%;
  height: 35px;
  font-size: 16px;
  transition: 0.2s linear;
}

.textInput:hover {
  cursor: pointer;
  transform: scale(1.05);
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}
</style>
