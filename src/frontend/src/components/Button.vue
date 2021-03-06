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
  computed: {
    loading() {
      return this.$store.getters.loading;
    },
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
    } else if (this.size == "big" && this.type == "cancel") {
      return "big-button cancel";
    } else if (this.size == "small" && this.type == "cancel") {
      return "button cancel";
    }
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

.loading {
  margin-left: 25%;
}
</style>
