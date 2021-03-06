<template>
  <div class="login">
    <img
      class="login-logo"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <TextInput
      id="umnetId"
      label="umnetId"
      ref="umnetId"
      :disable="loading"
    />
    <TextInput
      id="password"
      label="Password"
      ref="password"
      :disable="loading"
    />

    <Button
      class="login-button"
      id="button"
      label="Login"
      dest=""
      size="small"
      type="default"
      @click.native="login"
    />
    <router-link to="/createAccount" tag="a"
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
  methods: {
    login: function() {
      const umnetId = this.$refs.umnetId.inputData();
      const password = this.$refs.password.inputData();
      const values = { umnetId: umnetId, password: password };
      this.$store.dispatch("ACTION_LOGIN", values);
    },
  },
})
export default class LoginPage extends Vue {
  get loading() {
    return this.$store.getters.loading;
  }

  get userError() {
    return this.$store.getters.userError;
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.login {
  text-align: center;
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
