<template>
  <div class="create-account">
    <img
      class="create-account-image"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <TextInput id="umnetId" label="UMNetId" ref="umnetId" :disable="loading" />
    <TextInput
      id="password"
      label="Password"
      ref="password"
      :disable="loading"
      type="password"
    />

    <TextInput
      id="password2"
      label="Reenter Password"
      ref="password2"
      :disable="loading"
      type="password"
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
      class="create-account-button"
      id="create-account-button"
      label="Create Account"
      size="small"
      type="default"
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

.create-account {
  text-align: center;
  padding: $create-account-padding;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.create-account-button {
  margin-top: $create-account-button-margin-top;
  margin-bottom: $create-account-button-margin-bottom;
  width: $button-width;
  margin-left: auto;
  margin-right: auto;
}

.create-account-image {
  margin-bottom: $create-account-image-size;
  margin-top: $create-account-image-size;
}
</style>
