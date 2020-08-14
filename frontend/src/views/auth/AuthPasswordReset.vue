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
          <v-btn color="primary">Gravar senha</v-btn>
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
  }),
  methods: {
    on_password(password) {
      this.password = password;
      console.log("on_password", password);
    },
  },
  created() {
    let authorization = this.$route.query.authorization;
    if (!authorization) {
      alert("Sem autorização");
      this.$route.push("login");
    }
    //TODO: Obter autorização de alteração de senha do usuário
  },
};
</script>

<style></style>
