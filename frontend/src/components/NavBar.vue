<template>
  <v-app-bar app color="primary" dark>
    <div class="d-flex align-center">
      <a href="/f">
        <v-img alt="Scouts Logo" class="shrink mr-2" contain :src="scout_logo" width="50" />
      </a>
      <h1 class="d-none d-lg-block">Escoteirando</h1>
    </div>

    <v-spacer></v-spacer>

    <v-btn @click="testClick" text>
      <span class="mr-2">Test</span>
      <v-icon>mdi-open-in-new</v-icon>
    </v-btn>
    <NavBarUserMenu />
  </v-app-bar>
</template>

<script>
import NavBarUserMenu from "./NavBarUserMenu";
export default {
  components: { NavBarUserMenu },
  data: () => ({
    scout_logo: require("../assets/scouts_white.svg"),
  }),

  methods: {
    testClick() {
      this.$alert("Teste", "Título", "success");
    },
  },
};
</script>

<style></style>
