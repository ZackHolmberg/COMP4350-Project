<template>
  <div class="view-account">
    <h1 class="account-header">Account</h1>
    <div class="account-wrapper">
      <p class="label-text">First Name:</p>
      <TextInput
        id="account-first-name"
        class="view-account-text"
        :label="userFirstName"
        :disable="!editing"
        :edit="editing"
        ref="userFirstName"
      />
      <p class="label-text">Last Name:</p>
      <TextInput
        id="account-last-name"
        class="view-account-text"
        :label="userLastName"
        :disable="!editing"
        :edit="editing"
        ref="userLastName"
      />
      <p class="label-text">UMNetID:</p>
      <TextInput
        id="account-umnetId"
        class="view-account-text"
        :label="userUMnetId"
        :disable="true"
        ref="umnetId"
      />
      <p class="label-text">Password:</p>
      <TextInput
        id="account-password"
        class="view-account-text"
        :label="userPassword"
        :disable="!editing"
        :edit="editing"
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
// ViewAccountPage displays the user's account information, includer their password, UMNetID, and name. It also enables the user to edit their account information.
export default class ViewAccountPage extends Vue {
  data() {
    return {
      editing: false,
    }
  }

  // Retrieves the user's password from the store
  get userPassword() {
    return this.$store.getters.password;
  }
  // Retrieves the user's UMNetID from the store
  get userUMnetId() {
    return this.$store.getters.umnetId;
  }
  // Retrieves the user's first name from the store
  get userFirstName() {
    return this.$store.getters.firstName;
  }

  // Retrieves the user's last name from the store
  get userLastName() {
    return this.$store.getters.lastName;
  }

  // Sets the component's editing variable to the passed value
  setEditing(editing: boolean) {
    this.$data.editing = editing;
  }

  // Grabs the input entered into the three text inputs on the page, when the user is editing their information, and dispatches the update action with the data passed as an object in order
  // to update the user's information
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
  color: $default-text-color;
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
  font-size: $account-text-font-size;
  font-weight: bold;
  color: $default-text-color;
  width: $account-input-width;
  right: $account-input-right;
}

.label-text {
  position: absolute;
  left: $account-label-left;
  padding-top: $account-label-padding-top;
  font-size: $account-label-font-size;
  font-weight: bold;
  color: $default-text-color;
}
</style>
