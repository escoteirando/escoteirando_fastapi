<template>
  <div>
    <h1>Home</h1>
    <v-btn to="login">Login</v-btn>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("backend", ["getUser"]),
  },
  created() {
    const user = this.getUser;
    console.log("[HOME] user", user);
    if (user.ueb_id == 0 && !user.mappa_user) {
      console.log("[HOME] ASKING FOR MAPPA USER");
      this.$router.push({
        name: "mappa",
        query: { redirect: window.location.pathname },
      });
    }
  },
};
</script>

<style></style>
