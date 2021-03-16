<template>
  <div>
    <toggle-button
      id="mining"
      @change="onChange"
      v-model="miningValue"
      :value="miningValue"
      :sync="true"
      :color="{ checked: '#F2A900', unchecked: '#888888' }"
      :labels="{ checked: 'Mining On', unchecked: 'Mining Off' }"
      :width="300"
      :height="100"
      :font-size="32"
      :margin="10"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { ToggleButton } from "vue-js-toggle-button";

@Component({
  components: {
    ToggleButton,
  },
})
export default class Mining extends Vue {
  data() {
    return {
      miningValue: false,
    };
  }

  mounted() {
    this.$data.miningValue = this.$store.getters.mining;
  }

  onChange() {
    this.$store.commit("MUTATION_SET_MINING", this.$data.miningValue);
    this.$store.commit("MUTATION_SET_FIND_PROOF", this.$data.miningValue);
  }
}
</script>

<style lang="scss">
@import "../style.scss";
</style>
