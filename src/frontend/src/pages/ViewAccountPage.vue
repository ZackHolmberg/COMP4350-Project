<template>
  <div class="view-account">
    <h1 class="account-header">Account</h1>
    <div class="account-wrapper">
      <p id="account-name" class="view-account-text">
        Name: {{ userFirstName }} {{ userLastName }}
      </p>
      <p id="account-umnetId" class="view-account-text">
        UMnetId: {{ userUMnetId }} 
      </p>
      <p id="account-email" class="view-account-text">
        Email: {{ userUMnetId }}@myumanitoba.ca
      </p>
      <p id="account-password" class="view-account-text">
        Password: ********
      </p>
      <Button 
        id=account-cancel 
        class="account-cancel-button" 
        dest="/home" 
        label="Cancel" 
        size="small"
        type="cancel"
      />
      <Button 
        id=account-edit
        class="account-edit-button" 
        dest="/home" 
        label="Edit" 
        size="small"
        type="default"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Button from "../components/Button.vue";

@Component({
  components: {
    Button
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