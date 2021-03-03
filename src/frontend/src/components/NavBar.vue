<template>
  <div class="nav-bar">
    <img
      id="nav-logo"
      class="nav-logo"   
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <img
      id='nav-account'
      class="nav-account"
      alt="Account icon"
      src="../assets/accountIcon.png"
    />
    <img
      id="nav-settings"
      class="nav-settings"
      alt="Settings icon"
      src="../assets/settingsIcon.png"
    />
    <img
      id="nav-logout"
      class="nav-logout"
      alt="Logout icon"
      src="../assets/logoutIcon.png"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class NavBar extends Vue {
}
</script>

<style lang="scss">
@import "../style.scss";

.nav-logo {
  position: absolute;
  top: $nav-logo-top;
  left: $nav-logo-left; 
  width: $nav-logo-size;
  height: $nav-logo-size;
}

.nav-account {
  position: absolute;
  top: $account-icon-top; 
  right: $account-icon-right; 
  width: $account-icon-size; 
  height: $account-icon-size; 
  transition: $hover-transition;
}

.nav-account:hover {
  cursor: pointer;
  transform: $hover-transform-button;
}

.nav-settings {
  position: absolute;
  top: $settings-icon-top; 
  right: $settings-icon-right; 
  width: $settings-icon-size; 
  height: $settings-icon-size;
  transition: $hover-transition;
}

.nav-settings:hover {
  cursor: pointer;
  transform: $hover-transform-button;
}

.nav-logout {
  position: absolute;
  top: $logout-icon-top;
  right: $logout-icon-right;
  width: $logout-icon-size; 
  height: $logout-icon-size;
  transition: $hover-transition;
}

.nav-logout:hover {
  cursor: pointer;
  transform: $hover-transform-button;
}

.nav-bar {
  width: 100%;
  height: $nav-bar-height;
  background-color: $button-background-color;
  box-shadow: $box-shadow;
}
</style>
