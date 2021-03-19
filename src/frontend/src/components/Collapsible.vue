<template>
  <div>
    <Button 
      id="transaction-history-button" 
      dest="" 
      label="Transaction History" 
      size="long"
      type="other"
      @click.native="collapse"
    />
      <!------- OPENS COLLAPSIBLE ------->
      <div v-if="active" class="content">
        <TransactionHistory />
      </div>
      <!------- END -- OPENS COLLAPSIBLE ------->
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import TransactionHistory from "../components/TransactionHistory.vue";
import Button from "../components/Button.vue";

@Component({
  components: {
    TransactionHistory,
    Button
  },
})
export default class App extends Vue {
  @Prop() private question!: any;

  data() {
    return {
      active: false,
    }
  }

  collapse() {
    if(this.$data.active) {
      this.$data.active = false;
    }
    else {
      this.$data.active = true;
    }  
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.collapsible {
  border-radius: 10px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border: 2px solid black;
  background-color: white;
  color: black;
  cursor: pointer;
  padding: 18px;
  width: 800px;
  text-align: center;
  outline: none;
  font-size: 18px;
  transition: 0.2s linear;
}

.collapsible:hover {
  cursor: pointer;
  transform: scale(1.05);
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

.content {
  position: absolute;
  margin: auto;
  left: 2%;
  width: 90%;
  text-align: center;
  overflow: hidden;
  padding: 18px;
  display: 'none';
  background-color: lightgray;
  border-radius: 10px;
  border: 2px solid black;
  font-size: 18px;
}

.content-header {
  font-weight: bold;
  font-size: $big-button-font-size;
}
</style>
