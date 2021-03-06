<template>
  <div class="home">
    <img
      width="300px"
      height="300px"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <TextInput id="umnetId" label="umnetId" ref="umnetId" :disable="loading" />
    <TextInput
      id="password"
      label="Password"
      ref="password"
      :disable="loading"
    />

    <TextInput
      id="password2"
      label="Reenter Password"
      ref="password2"
      :disable="loading"
    />

    <TextInput
      id="first-name"
      label="First Name"
      ref="firstName"
      :disable="loading"
    />

    <TextInput
      id="last-name"
      label="Last Name"
      ref="lastName"
      :disable="loading"
    />

    <Button
      class="login-button"
      id="create-account-button"
      dest=""
      label="Create Account"
      @click.native="createAccount"
    />
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
export default class CreateAccountPage extends Vue {
  createAccount() {
    const umnetId = this.$refs.umnetId.inputData();
    const password = this.$refs.password.inputData();
    const password2 = this.$refs.password2.inputData();
    const firstName = this.$refs.firstName.inputData();
    const lastName = this.$refs.lastName.inputData();
    const values = {
      umnetId: umnetId,
      password: password,
      password2: password2,
      firstName: firstName,
      lastName: lastName,
    };
    this.$store.dispatch("ACTION_CREATE_ACCOUNT", values);
  }
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
