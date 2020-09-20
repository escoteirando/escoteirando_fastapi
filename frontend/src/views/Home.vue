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
    const user = await this.API.AUTH.getLoggedUser();

    if (!user) {
      this.$router.push({ name: "login" });
      return;
    }
    if (user.ueb_id == 0 && !user.mappa_user) {
      console.log("[HOME] ASKING FOR MAPPA USER");
      const that = this;
      this.$confirm(
        "Você deseja integrar as informações do mAPPa Adulto?",
        "Atenção",
        "question"
      ).then(function (r) {
        if (r) {
          that.$router.push({
            name: "mappa",
            query: { redirect: window.location.pathname },
          });
        }
      });
    }
    console.log("[MAPPA] progressões", this.API.MAPPA.getTodasProgressoes());
    this.LoadUserCards();
  },
  methods: {
    async LoadUserCards() {
      let cards = await this.API.USER.getUserCards();
      if (cards) {
        this.cards = cards;
      }
    },
  },
};
</script>

<style></style>
