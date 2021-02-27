<template>
  <div class="home">
    <img
      width="300px"
      height="300px"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <TextInput id="username" label="Username" />
    <TextInput id="password" label="Password" />
    <Button
      class="login-button"
      id="button"
      dest="/home"
      label="Login"
    />
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
export default class LoginPage extends Vue {
}
</script>

<style lang="scss">
@import "../style.scss";

.home {
  text-align: center;
  padding: 25px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.login-button {
  margin-top: 100px;
  margin-bottom: 50px;
}

body {
  background-color: $background-color;
}

img {
  margin-bottom: 100px;
  margin-top: 100px;
}

a {
  color: $link-color;
}
</style>
