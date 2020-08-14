<template>
  <v-footer dark padless>
    <v-card class="flex" flat tile>
      <v-card-title class="primary">
        <strong class="subheading">Get connected with us on social networks!</strong>

        <v-spacer></v-spacer>

        <v-btn v-for="icon in icons" :key="icon" class="mx-4" dark icon>
          <v-icon size="24px">{{ icon }}</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="py-2 white--text text-center">
        {{ new Date().getFullYear() }}&nbsp;|
        <strong>Escoteirando</strong>&nbsp;|
        <ComplianceTextButton is_text document="usage_terms" />&nbsp;|
        <ComplianceTextButton is_text document="privacy_policy" />&nbsp;|
        <ComplianceTextButton is_text document="who_are_us" />&nbsp;|
        <v-icon
          v-if="development"
          color="orange darken-2"
          title="Ambiente de desenvolvimento"
        >mdi-test-tube</v-icon>
        <v-icon v-else color="green darken-2" title="Ambiente de produção">mdi-check-outline</v-icon>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
import ComplianceTextButton from "./ComplianceTextButton";
import { ENVIRONMENT } from "../api/consts";
export default {
  components: { ComplianceTextButton },
  data: () => ({
    icons: [
      "mdi-facebook",
      "mdi-twitter",
      "mdi-linkedin",
      "mdi-instagram",
      "mdi-github",
    ],
    development: ENVIRONMENT == "DEVELOPMENT",
  }),
};
</script>

<style></style>
