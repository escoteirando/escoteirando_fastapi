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

    <v-btn @click="testClick" text>
      <span class="mr-2">Test</span>
      <v-icon>mdi-open-in-new</v-icon>
    </v-btn>
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
    testClick() {
      this.$alert("Teste", "Título", "success");
    },
    goHome() {
      if (this.$router.history.current.name != "home") {
        this.$router.push({ name: "home" });
      }
    },
  },
};
</script>
