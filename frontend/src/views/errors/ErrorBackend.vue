<template>
  <div class="NotFound">
    <v-container>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card height="400" color="transparent" flat>
            <div class="display-3 mt-5">Backend indisponível!</div>
            <div class="grey--text lighten-5">
              <p
                v-if="!internetOnline"
              >Hmm. Parece que sua conexão com a internet também não está OK</p>
            </div>
            <v-card-text v-if="automaticTesting">
              Tentativa {{autoRetryCount}} de {{maxAutoTests}} de conexão ao backend...
              <v-progress-circular
                :rotate="270"
                :size="100"
                :width="15"
                :value="progressValue"
                color="red"
              >{{ timeLeft }}</v-progress-circular>
            </v-card-text>
            <v-card-text v-else>
              Tentamos conectar ao backend por {{maxAutoTests}} vezes, sem sucesso.
              <br />
            </v-card-text>
            <v-card-actions>
              <v-btn v-if="!automaticTesting" @click="doRetry" color="error">
                <v-icon left>mdi-repeat</v-icon>Tente novamente
              </v-btn>
              <v-btn @click="quemEBackend" color="info">
                Mas afinal, o que é esse tal de backend
                <v-icon>mdi-help-network</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      automaticTesting: true,
      autoRetryCount: 0,
      intervalBetweenTests: 5,
      maxAutoTests: 3,
      iteration: 0,
      redirect: null,
      internetOnline: false,
    };
  },
  computed: {
    progressValue() {
      return 100 - 100 * (this.iteration / this.intervalBetweenTests);
    },
    timeLeft() {
      return this.intervalBetweenTests - this.iteration;
    },
  },
  methods: {
    async testBackend() {
      try {
        this.internetOnline = navigator.onLine;
        let response = await window.axios.get("/api/hc");
        if (response.status == 200) {
          console.log("BACKEND", response.data);
          return true;
        }
      } catch (error) {
        console.error("BACKEND OFFLINE");
      }
      return false;
    },
    async doTestBackend() {
      this.iteration++;
      if (this.iteration > this.intervalBetweenTests) {
        if (await this.testBackend()) {
          this.backToRoute();
          return;
        }
        this.iteration = 0;
        this.autoRetryCount++;
      }
      if (this.autoRetryCount <= this.maxAutoTests) {
        setTimeout(this.doTestBackend, 1000);
        return;
      }
      this.automaticTesting = false;
    },
    backToRoute() {
      const redirect = this.redirect
        ? { path: this.redirect }
        : { name: "home" };
      console.log("[BACKEND] RETURNING AFTER OFFLINE", redirect);

      this.$router.push(redirect);
    },
    async doRetry() {
      this.iteration = 0;
      this.autoRetryCount = 1;
      this.automaticTesting = true;
      if (await this.doTestBackend()) {
        this.backToRoute();
      } else {
        setTimeout(this.doTestBackend, 1000);
      }
    },
    quemEBackend() {
      this.$alert(
        "Backend é o sistema que roda 'por trás' dessa tela bonita, e processa todas as informações que você vê por aqui.",
        "Quem é o backend?",
        "question"
      );
    },
  },
  mounted() {
    this.internetOnline = navigator.onLine;
    this.redirect = this.$route.query.redirect;
    this.autoRetryCount = 1;
    this.doTestBackend();
  },
};
</script>

<style scoped>
.paragraph-text {
  font-size: 18px;
}
.v-progress-circular {
  margin: 1rem;
}
</style>