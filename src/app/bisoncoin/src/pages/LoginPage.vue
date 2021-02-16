<template>
  <div class="home">
    <img
      width="300px"
      height="300px"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <TextInput label="Username" />
    <TextInput label="Password" />
    <Button label="Login" />
    <!-- TODO: Move this text and other hardcoded text to a separate file, as well as colours -->
    <a href="TODO">Don't have an account? Create one now!</a>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TextInput from "../components/TextInput.vue";
import Button from "../components/Button.vue";

@Component({
  components: {
    TextInput,
    Button,
  },
})
export default class LoginPage extends Vue {}
</script>

<style>
.home {
  padding: 25px;
}

body {
  background-color: lightgray;
}

img {
  margin-bottom: 100px;
  margin-top: 100px;
}
</style>
