<template>
  <div>
    <router-link :to="dest" v-bind:class="getClass()" tag="button">
      <Circle2 class="loading" v-if="loading" />
      <span v-else>{{ label }}</span></router-link
    >
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import Circle2 from "vue-loading-spinner/src/components/Circle2.vue";

@Component({
  components: {
    Circle2,
  },
})
export default class Button extends Vue {
  @Prop() private label!: string;
  @Prop() private dest!: string;
  @Prop() private size!: string;
  @Prop() private type!: string;

  getClass() {
    if (this.size == "big" && this.type == "default") {
      return "big-button default";
    } else if (this.size == "small" && this.type == "default") {
      return "button default";
    } else if (this.size == "long" && this.type == "other") {
      return "long-button other";
    } else if (this.size == "big" && this.type == "cancel") {
      return "big-button cancel";
    } else if (this.size == "small" && this.type == "cancel") {
      return "button cancel";
    }
  }

  get loading() {
    return this.$store.getters.loading;
  }
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

.other {
  background-color: rgba(173, 2, 59, 0.521);
}

.big-button {
  width: $big-button-width;
  height: $big-button-height;
  border-radius: $big-button-border-radius;
  box-shadow: $box-shadow;
  font-size: $big-button-font-size;
  font-family: $default-font;
  transition: $hover-transition;
  border: $border-color;
  color: $button-text;
}

.long-button {
  width: 85%;
  height: $big-button-height;
  border-radius: $big-button-border-radius;
  box-shadow: $box-shadow;
  font-size: $big-button-font-size;
  font-family: $default-font;
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
  font-family: $default-font;
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

.long-button:hover {
  cursor: pointer;
  transform: scale(1.1);
  box-shadow: $box-shadow-hover;
}

.loading {
  margin-left: $loading-spinner-margin;
}
</style>
