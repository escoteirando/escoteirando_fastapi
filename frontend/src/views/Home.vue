<template>
  <v-container fluid>
    <v-row dense>
      <HomeCard v-for="card in cards" :key="card.title" :card="card" />
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import HomeCard from "../components/HomeCard";
export default {
  components: { HomeCard },
  data: function () {
    return { cards: [] };
  },
  computed: {
    ...mapGetters("backend", ["getUser", "getHost"]),
    swagger() {
      return this.getHost + "/docs";
    },
  },
  async mounted() {
    console.log("[VIEW HOME] MOUNTED");
    const user = await this.API.AUTH.getLoggedUser();

    if (!user) {
      this.$router.push({ name: "login" });
      return;
    }
    console.log("[HOME] user", user);
    if (user.ueb_id == 0 && !user.mappa_user) {
      console.log("[HOME] ASKING FOR MAPPA USER");
      this.$prompt(
        "Você deseja integrar as informações do mAPPa Adulto?",
        "Atenção",
        "question"
      ).then(function (r) {
        if (r) {
          this.$router.push({
            name: "mappa",
            query: { redirect: window.location.pathname },
          });         
        }
      });
    }
    this.LoadUserCards();
  },
  methods: {
    LoadUserCards() {
      window.axios
        .get("/api/user/home")
        .then((response) => {
          this.cards = response.data;
          this.cards.push({ title: "Login", route: "login", flex: 4 });
          this.cards.push({ title: "Swagger", route: this.swagger, flex: 4 });
        })
        .catch((error) => console.error("[HOME] CARDS", error));
    },
  },
};
</script>

<style></style>
