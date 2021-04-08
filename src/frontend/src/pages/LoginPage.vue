<template>
  <div class="login">
    <img
      class="login-logo"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <TextInput id="umnetId" label="UMNetId" ref="umnetId" :disable="loading" />
    <TextInput
      id="password"
      label="Password"
      ref="password"
      type="password"
      :disable="loading"
    />

    <Button
      class="login-button"
      id="login-button"
      label="Login"
      size="small"
      type="default"
      @click.native="login"
    />

    <router-link
      class="create-account-link"
      to="/createAccount"
      id="create-account-link"
      tag="a"
      >Don't have an account? Create one now!</router-link
    >
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

// LoginPage is where users enter their credentials in order to log in to the application
export default class LoginPage extends Vue {
  // Retrieves the state's loading value from the store
  get loading() {
    return this.$store.getters.loading;
  }

  // Grabs the input entered into the two text inputs on the page and dispatches the login action with the data passed as an object
  login() {
    const umnetId = this.$refs.umnetId.inputData();
    const password = this.$refs.password.inputData();
    const values = { umnetId: umnetId, password: password };
    this.$store.dispatch("ACTION_LOGIN", values);
  }
}
</script>

// STYLING
<style lang="scss">
@import "../style.scss";

.login {
  text-align: center;
  -webkit-font-smoothing: antialiased;
}

.login-button {
  margin-top: $login-button-margin;
  margin-bottom: $login-button-margin;
  width: $button-width;
  margin-left: auto;
  margin-right: auto;
}

.login-logo {
  margin-bottom: $login-logo-margin;
  margin-top: $login-logo-margin;
  width: $login-logo-size;
  height: $login-logo-size;
}

.create-account-link {
  color: $link-color;
  font-size: $link-font-size;
  font-weight: bold;
}
</style>
