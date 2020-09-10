<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Autorização mAPPa</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              id="mappa_user"
              label="Usuário mAPPa"
              name="mappa_user"
              prepend-icon="mdi-account-circle"
              type="text"
              v-model="mappa_user"
              readonly
            />
            <v-text-field
              id="auth_valid"
              label="Autorização válida até"
              name="auth_valid"
              prepend-icon="mdi-calendar-clock"
              type="text"
              v-model="authValidText"
              readonly
            />
            <v-text-field
              v-if="!authValid"
              id="senha"
              label="Senha"
              name="senha"
              prepend-icon="mdi-key"
              type="password"
              v-model="mappa_password"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <ComplianceTextButton v-if="!authValid" document="auth_mappa" />
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="botaoClick">{{botaoText}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import { currentTimeStamp } from "../../plugins/local_storage";
import ComplianceTextButton from "../../components/ComplianceTextButton";
export default {
  components: { ComplianceTextButton },
  data() {
    return {
      mappa_user: null,
      mappa_auth: null,
      mappa_valid_until: 0,
      mappa_password: null,
      redirect: null,
    };
  },
  computed: {
    ...mapGetters("backend", ["getUser"]),
    authValid() {
      return this.mappa_valid_until > currentTimeStamp();
    },
    authValidText() {
      return !this.authValid
        ? "Expirada"
        : new Date(this.mappa_valid_until * 1000).toLocaleString();
    },
    botaoText() {
      return this.authValid ? "OK" : "Reativar";
    },
  },
  mounted() {
    const that = this;
    if (!this.getUser.mappa_user) {
      this.$alert("Não há registro de usuário mAPPa para você!").then(() => {
        that.$router.push({ name: "mappa" });
      });
      return;
    }
    this.redirect = this.$route.query.redirect;
    this.mappa_user = this.getUser.mappa_user;
    this.mappa_valid_until = this.getUser.mappa_valid_until;
    this.mappa_auth = this.getUser.mappa_auth;
  },
  methods: {
    botaoClick() {
      if (this.authValid) {
        this.goHome();
      } else {
        if (!this.mappa_password) {
          this.$alert(
            "Você deve informar a senha para acesso ao mAPPa",
            "Atenção",
            "error"
          );
          return;
        }
        this.API.MAPPA.login(this.mappa_user, this.mappa_password)
          .then((response) => {
            console.log("[MAPPA LOGIN]", response);
          })
          .catch((error) => {
            console.error("[MAPPA LOGIN]", error);
          });
      }
    },
    goHome() {
      if (this.redirect) {
        this.$router.push(this.redirect);
      } else {
        this.$router.push({ name: "home" });
      }
    },
  },
};
</script>

<style>
</style>