<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Perfil do usuário</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              id="mappa_user"
              label="Usuário mAPPa"
              name="mappa_user"
              prepend-icon="mdi-account-circle"
              type="text"
              v-model="user.mappa_username"
              append-outer-icon="mdi-login-variant"
              @click:append-outer="loginMappa"
            />
            <v-text-field
              id="name"
              label="Nome"
              name="full_name"
              prepend-icon="mdi-account"
              type="text"
              v-model="user.full_name"
            />
            <v-text-field
              id="email"
              label="Email"
              name="email"
              prepend-icon="mdi-at"
              type="email"
              :rules="rules.email"
              v-model="user.email"
            />

            <v-text-field
              id="nascimento"
              label="Data de nascimento"
              name="nascimento"
              prepend-icon="mdi-cake"
              type="date"
              v-model="user.nascimento"
              :rules="rules.nascimento"
              :readonly="!!user.mappa_username"
              :hint="mappaFieldHint"
            />
            <v-select
              id="gender"
              label="Gênero"
              name="gender"
              prepend-icon="mdi-gender-male-female"
              :items="genders"
              item-text="text"
              item-value="id"
              v-model="user.gender"
              :readonly="!!user.mappa_username"
              :hint="mappaFieldHint"
            />
            <v-select
              id="ramo"
              label="Ramo"
              name="ramo"
              prepend-icon="mdi-leaf"
              :items="ramos"
              item-text="text"
              item-value="id"
              v-model="user.ramo"
              :readonly="!!user.mappa_username"
              :hint="mappaFieldHint"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" :disabled="!podeGravar" @click="gravar">Gravar</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import { getDictAsList } from "../../api/dicionario";
const idadeMinima = 18;
const aniversarioMaximo = new Date(
  new Date().getFullYear() - idadeMinima,
  new Date().getMonth(),
  new Date().getDay()
)
  .toISOString()
  .substring(0, 10);
const aniversarioMinimo = new Date(
  new Date().getFullYear() - 100,
  new Date().getMonth(),
  new Date().getDay()
)
  .toISOString()
  .substring(0, 10);
export default {
  data: () => ({
    user: {
      full_name: "",
      email: "",
      nascimento: new Date().toISOString().substring(0, 10),
      mappa_username: "guionardo",
      gender: "M",
      ramo: "A",
    },
    rules: {
      nascimento: [
        (value) => !!value || "Data de nascimento é requerida",
        (value) =>
          value < aniversarioMaximo ||
          `Você deve ter mais de ${idadeMinima} anos`,
        (value) =>
          value > aniversarioMinimo || `Você deve estar vivo pra continuar`,
      ],
      email: [
        (v) => !!v || "E-mail é obrigatório",
        (v) => /.+@.+\..+/.test(v) || "E-mail deve ser válido",
      ],
    },
    genders: getDictAsList('sexo'),
    ramos: getDictAsList("ramo"),
  }),
  computed: {
    ...mapGetters("backend", ["getUser"]),
    isMappaUser() {
      return this.user.mappa_username && this.user.mappa_username.length > 0;
    },
    podeGravar() {
      return (
        this.user.nascimento > aniversarioMinimo &&
        this.user.nascimento < aniversarioMaximo
      );
    },
    mappaFieldHint() {
      return this.user.mappa_username ? "Informação obtida do mAPPa" : "";
    },
  },
  mounted() {
    console.log("[UserProfile] mounted");
    this.user.full_name = this.getUser.full_name || this.getUser.name;
    this.user.email = this.getUser.email;
    this.user.nascimento = this.getUser.nascimento.substring(0, 10);
  },
  methods: {
    async gravar() {
      const profileRequest = {
        name: this.user.full_name,
        mappa_user: this.user.mappa_username,
        email: this.user.email,
        nascimento: this.user.nascimento,
        sexo: this.user.gender,
        ramo: this.user.ramo,
      };
      console.log("GRAVAR", profileRequest);
      let response = await this.API.USER.saveProfile(profileRequest);
      if (response.ok) {
        this.$alert(
          "Dados do usuário foram gravados com sucesso!",
          "Sucesso",
          "success"
        );
        this.API.AUTH.verifyLoggedUser(true);
        this.$router.push({ name: "home" });
      } else {
        this.$alert(
          "Dados do usuário não foram gravados: " + response.msg,
          "Atenção",
          "error"
        );
      }
    },
    loginMappa() {
      const that = this;
      if (!this.user.mappa_username) {
        this.$alert("Informe o usuário mAPPa!", "Atenção", "warning");
        return;
      }
      this.$prompt(
        "Informe a senha do usuário " + this.user.mappa_username,
        "",
        "Acesso ao mAPPa",
        "question",
        { input: "password" }
      )
        .then((r) => {
          that.API.MAPPA.login(that.user.mappa_username, r)
            .then((response) => {
              that.user.email = that.user.email || response.email;
            })
            .catch((error) => {
              console.error("[USERPROFILE] MAPPA_LOGIN", error);
            });
        })
        .catch((error) => {
          console.error("[USERPROFILE] SENHA MAPPA", error);
          that.$alert("Senha não foi informada!", "Atenção", "warning");
        });
    },
  },
};
</script>

<style>
</style>