<template>
  <div class="nav-bar">
    <!-- Bisoncoin logo -->
    <img
      id="nav-logo"
      class="nav-logo"
      alt="BisonCoin logo"
      src="../assets/BisonCoin.png"
    />
    <!-- End -- Bisoncoin logo -->
    <!-- Account -->
    <router-link to="/account">
      <img
        id="nav-account"
        class="nav-account"
        alt="Account icon"
        src="../assets/accountIcon.png"
      />
    </router-link>
    <!-- End -- Account -->
    <!-- Logout -->
    <div @click="logout">
      <img
        id="nav-logout"
        class="nav-logout"
        alt="Logout icon"
        src="../assets/logoutIcon.png"
      />
    </div>
    <!-- End -- Logout -->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class NavBar extends Vue {
  // Dispatches logout action if user clicks logout symbol
  logout() {
    this.$store.dispatch("ACTION_LOGOUT");
  }
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
