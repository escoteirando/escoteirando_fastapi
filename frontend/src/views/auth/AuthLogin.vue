<template>
  <v-row align="center" justify="center">
    <v-snackbar v-model="alert" centered multi-line color="error" timeout="5000">
      {{ alertMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn dark text v-bind="attrs" @click="alert = false">X</v-btn>
      </template>
    </v-snackbar>
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Login</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              id="user"
              label="Usuário"
              name="user"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
              required
            />
            <PasswordField v-on:password="on_password" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text small to="subscribe">Registrar</v-btn>
          <v-btn text small to="reset">Esqueci a senha</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="doLogin" :disabled="!canLogin">Login</v-btn>
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
    redirect: null,
    alert: false,
    alertMessage: "",
  }),
  computed: {
    canLogin() {
      return this.username && this.password;
    },
  },
  mounted() {
    this.redirect = this.$route.query.redirect;
  },
  methods: {
    doLogin() {
      this.API.AUTH.login(this.username, this.password)
        .then((response) => {
          console.log("LOGIN", response);
          this.$router.push(this.redirect || "home");
        })
        .catch((error) => {
          this.alertMessage = error.response.data.message;
          this.alert = true;
        });
    },
    on_password(password) {
      this.password = password;
    },
  },
};
</script>

<style></style>
