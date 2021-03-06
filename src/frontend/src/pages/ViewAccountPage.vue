<template>
  <div class="view-account">
    <h1 class="account-header">Account</h1>
    <div class="account-wrapper">
      <TextInput
        id="account-first-name"
        class="view-account-text"
        :label="userFirstName"
        :disable="!editing"
        ref="userFirstName"
      />

      <TextInput
        id="account-last-name"
        class="view-account-text"
        :label="userLastName"
        :disable="!editing"
        ref="userLastName"
      />
      <TextInput
        id="account-umnetId"
        class="view-account-text"
        :label="userUMnetId"
        :disable="true"
        ref="umnetId"
      />
      <TextInput
        id="account-password"
        class="view-account-text"
        :label="userPassword"
        :disable="!editing"
        ref="userPassword"
      />

      <Button
        id="account-cancel"
        class="account-cancel-button"
        dest="/home"
        label="Cancel"
        size="small"
        type="cancel"
      />
      <Button
        v-if="!editing"
        id="account-edit"
        class="account-edit-button"
        dest="/account"
        label="Edit"
        size="small"
        type="default"
        @click.native="setEditing(true)"
      />
      <Button
        v-else
        id="account-save"
        class="account-edit-button"
        dest="/account"
        label="Save Changes"
        size="small"
        type="default"
        @click.native="saveChanges"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Button from "../components/Button.vue";
import TextInput from "../components/TextInput.vue";

@Component({
  components: {
    Button,
    TextInput,
  },
})
export default class ViewAccountPage extends Vue {
  get userPassword() {
    return this.$store.getters.password;
  }

  get userUMnetId() {
    return this.$store.getters.umnetId;
  }

  get userFirstName() {
    return this.$store.getters.firstName;
  }

  get userLastName() {
    return this.$store.getters.lastName;
  }

  get editing() {
    return this.$store.getters.editing;
  }

  setEditing(editing: boolean) {
    console.log("setting editing to:", editing);
    this.$store.commit("MUTATATION_SET_EDITING", editing);
  }

  saveChanges() {
    const password = this.$refs.userPassword.inputData();
    const firstName = this.$refs.userFirstName.inputData();
    const lastName = this.$refs.userLastName.inputData();
    const values = {
      password: password,
      firstName: firstName,
      lastName: lastName,
    };
    this.setEditing(false);
    this.$store.dispatch("ACTION_UPDATE_USER", values);
  }
}
</script>

<style lang="scss">
@import "../style.scss";

.account-header {
  font-size: $default-header-font-size;
  text-align: center;
  font-weight: bold;
}

.account-wrapper {
  position: absolute;
  top: $account-wrapper-top;
  left: 0;
  right: 0;
  margin: auto;
  padding: 1%;
  text-align: center;
  width: $account-wrapper-width;
}

.view-account {
  -webkit-font-smoothing: antialiased;
}

.account-edit-button {
  position: absolute;
  left: $account-button-position;
  padding: $account-button-padding;
}

.account-cancel-button {
  position: absolute;
  right: $account-button-position;
  padding: $account-button-padding;
}

.view-account-text {
  position: relative;
  padding-top: $account-text-padding-top;
  font-size: $account-text-font-size;
  font-weight: bold;
  color: $default-text-color;
}
</style>
