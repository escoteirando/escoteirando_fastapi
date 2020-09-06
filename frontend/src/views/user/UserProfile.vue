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
              id="user_mappa"
              label="Usuário mAPPa"
              name="user_mappa"
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
              v-model="user.email"
            />

            <v-text-field
              id="birthday"
              label="Data de nascimento"
              name="birthday"
              prepend-icon="mdi-cake"
              type="date"
              v-model="user.birthday"
              :rules="rules.birthday"
              :readonly="!!user.mappa_username"
              :hint="user.mappa_username?'Informação obtida do mAPPa':''"
            />
            <v-select
              id="gender"
              label="Gênero"
              name="gender"
              prepend-icon="mdi-gender-male-female"
              :items="genders"
              item-text="text"
              item-value="code"
              v-model="user.gender"
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
import { tipos_ramos } from "../../api/consts";
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
      birthday: new Date().toISOString().substring(0, 10),
      mappa_username: "guionardo",
      gender: "M",
      ramo: "A",
    },
    rules: {
      birthday: [
        (value) => !!value || "Data de nascimento é requerida",
        (value) =>
          value < aniversarioMaximo ||
          `Você deve ter mais de ${idadeMinima} anos`,
        (value) =>
          value > aniversarioMinimo || `Você deve estar vivo pra continuar`,
      ],
    },
    genders: [
      { code: "M", text: "Masculino" },
      { code: "F", text: "Feminino" },
      { code: "O", text: "Outro" },
    ],
    ramos: tipos_ramos,
  }),
  computed: {
    ...mapGetters("backend", ["getUser"]),
    isMappaUser() {
      return this.user.mappa_username && this.user.mappa_username.length > 0;
    },
    podeGravar() {
      return (
        this.user.birthday > aniversarioMinimo &&
        this.user.birthday < aniversarioMaximo
      );
    },
  },
  mounted() {
    this.user.full_name = this.getUser.full_name || this.getUser.name;
    this.user.email = this.getUser.email;
  },
  methods: {
    gravar() {
      console.log("GRAVAR");
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
          that.MAPPA.login(that.user.mappa_username, r)
            .then((response) => {
              that.user.email = that.user.email || response.email
            })
            .catch((error) => {});
        })
        .catch(() => {
          that.$alert("Senha não foi informada!", "Atenção", "warning");
        });
    },
  },
};
</script>

<style>
</style>