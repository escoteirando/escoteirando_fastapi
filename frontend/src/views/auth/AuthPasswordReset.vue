<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Nova senha</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              id="user"
              label="Usuário/e-mail"
              name="user"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
              readonly
            />
            <PasswordField v-on:password="on_password" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" :disabled="!podeGravar" @click="mandaGravar">Gravar senha</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import PasswordField from "../../components/PasswordField";

export default {
  components: { PasswordField },
  data: () => ({
    username: "",
    password: "",
    chave: "",
  }),
  computed: {
    podeGravar() {
      return this.password && this.username && this.chave;
    },
  },
  methods: {
    on_password(password) {
      this.password = password;
      console.log("on_password", password);
    },
    mandaGravar() {
      const that = this;
      window.axios
        .post("/auth/password/reset", {
          authorization: this.chave,
          email: this.username,
          password: this.password,
        })
        .then(() => {
          that.$alert("Senha redefinida com sucesso!").then(() => {
            that.$router.push("login");
          });
        })
        .catch((error) => {
          that.$alert("Não foi possível redefinir a senha: " + error.response.data.msg);
        });
    },
  },
  created() {
    let chave = this.$route.query.chave;
    const that = this;
    if (!chave) {
      this.$alert(
        "Acesso não autorizado sem uma chave de redefinição de senha!"
      ).then(function () {
        that.$router.push("login");
      });
      return;
    }

    window.axios
      .get("/auth/password/" + chave)
      .then((response) => {
        that.username = response.data.data.email;
        that.chave = chave;
      })
      .catch(() => {
        that
          .$alert("Chave de redefinição inválida ou expirada!")
          .then(function () {
            that.$rounter.push("login");
          });
      });
    //TODO: Obter autorização de alteração de senha do usuário
  },
};
</script>

<style></style>
