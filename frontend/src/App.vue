<template>
  <v-app>
    <NavBar />

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <Footer />
  </v-app>
</template>

<script>
// import HelloWorld from "./components/HelloWorld";
// import AuthLogin from "./views/AuthLogin";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
export default {
  name: "App",

  components: {
    // HelloWorld,
    // AuthLogin,
    NavBar,
    Footer,
  },

  data: () => ({
    //
  }),
};
</script>
