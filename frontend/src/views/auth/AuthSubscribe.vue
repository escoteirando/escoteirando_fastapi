<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Registrar</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              id="user"
              label="Usuário"
              :counter="20"
              :rules="userRules"
              name="user"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
              required
            />

            <v-text-field
              id="email"
              label="E-mail"
              name="email"
              prepend-icon="mdi-email"
              type="email"
              v-model="email"
              :rules="emailRules"
              required
            />

            <PasswordField v-on:password="on_password" />
            <v-checkbox
              v-model="agree"
              :rules="[(v) => !!v || 'Você deve concordar para continuar!']"
              label="Você concorda com os termos de uso?"
              required
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <ComplianceTextButton document="usage_terms" />
          <v-spacer></v-spacer>
          <v-btn color="primary" :disabled="!canRegister" @click="doRegistrar">Registrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import ComplianceTextButton from "../../components/ComplianceTextButton";
import PasswordField from "../../components/PasswordField";
import getUserMessage from "../../i18/user_messages";

import {
  isValidEmail,
  userNameRules,
  isValidUserName,
  isValidPassword,
} from "../../api/tools";

export default {
  components: { ComplianceTextButton, PasswordField },
  data: () => ({
    username: "",
    userRules: [
      (v) => isValidUserName(v) || userNameRules,
      (v) => !isValidEmail(v) || "Nome de usuário não pode ser um e-mail",
    ],
    email: "",
    emailRules: [(v) => isValidEmail(v) || "E-mail deve ser válido"],
    password: "",
    agree: false,
    valid: true,
  }),
  computed: {
    canRegister() {
      return (
        isValidUserName(this.username) &&
        isValidEmail(this.email) &&
        isValidPassword(this.password) &&
        this.agree
      );
    },
  },
  methods: {
    on_password(password) {
      this.password = password;
    },
    doRegistrar() {
      this.API.AUTH.subscribe(this.username, this.email, this.password)
        .then((response) => {
          if (!response.data.ok) {
            console.error("REGISTRAR", response.data);
            this.$fire({
              title: getUserMessage(response.data.code),
              icon: "error",
              text: response.data.msg,
            });
          } else {
            console.log("REGISTRAR", response.data);
            this.$fire({
              title: getUserMessage(response.data.code),
              icon: "success",
              text: response.data.msg,
            });
          }
        })
        .catch((error) => {
          console.error("REGISTRAR", error);
        });
    },
  },
};
</script>

<style></style>
