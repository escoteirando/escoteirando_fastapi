<template>
  <v-app-bar app color="primary" dark>
    <div class="d-flex align-center">
      <v-img
        alt="Scouts Logo"
        class="shrink mr-2"
        @click="goHome"
        contain
        :src="scout_logo"
        width="50"
      />
      <h1 class="d-none d-lg-block">Escoteirando</h1>
    </div>

    <v-spacer></v-spacer>
   
    <NavBarTestMenu />
    <NavBarUserMenu />
  </v-app-bar>
</template>

<script>
import NavBarUserMenu from "./NavBarUserMenu";
import NavBarTestMenu from "./NavBarTestMenu";
export default {
  components: { NavBarUserMenu, NavBarTestMenu },
  data: () => ({
    scout_logo: require("../assets/scouts_white.svg"),
  }),

  methods: {
    goHome() {
      if (this.$router.history.current.name != "home") {
        this.$router.push({ name: "home" });
      }
    },
  },
};
</script>
