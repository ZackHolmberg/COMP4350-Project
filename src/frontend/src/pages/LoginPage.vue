<template>
  <div class="login">
    <img
      class="login-logo"
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
      size="small"
      type="default"
    />
    <a class="create-account-link" href="TODO">Don't have an account? Create one now!</a>
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

.login {
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.login-button {
  margin-top: $login-button-margin-top;
  margin-bottom: $login-button-margin-bottom;
}

.login-logo {
  margin-bottom: $login-logo-margin;
  margin-top: $login-logo-margin;
  width: $login-logo-size;
  height: $login-logo-size;
}

.create-account-link {
  color: $link-color;
}
</style>
