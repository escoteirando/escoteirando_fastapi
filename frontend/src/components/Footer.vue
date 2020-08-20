<template>
  <v-footer dark padless>
    <v-card class="flex" flat tile>
      <v-card-title class="primary">
        <a
          v-for="link in left_links"
          :key="link.href"
          :href="link.href"
          :title="link.title"
          target="_empty"
        >
          <v-img :alt="link.alt" class="shrink mr-2" contain :src="link.src" width="40" />
        </a>

        <v-spacer></v-spacer>

        <v-btn v-for="link in links" :key="link.url" class="mx-4" dark icon :href="link.url">
          <v-icon size="24px" :title="link.title">{{ link.icon }}</v-icon>
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
    links: [
      {
        icon: "mdi-github",
        url: "https://github.com/guionardo",
        title: "GitHub Guionardo",
      },
      {
        icon: "mdi-linkedin",
        url: "https://www.linkedin.com/in/guionardo/",
        title: "LinkedIn",
      },
    ],
    left_links: [
      {
        src: require("../assets/escoteiros.svg"),
        href: "https://escoteiros.org.br",
        alt: "Escoteiros Logo",
        title: "Escoteiros do Brasil",
      },
      {
        src: require("../assets/scouts.svg"),
        href: "https://scout.org",
        alt: "Scouts Logo",
        title: "Scouts",
      },{
        src:require("../assets/logo_mappa_redondo.svg"),
        href:"#",
        alt:"mAPPa logo",
        title:"mAPPa Adulto"
      }
    ],
    development: ENVIRONMENT == "DEVELOPMENT",
  }),
};
</script>

<style></style>
