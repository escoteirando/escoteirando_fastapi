<template>
  <v-dialog v-model="dialog" max-width="80%">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="primary"
        dark
        v-bind="attrs"
        v-on="on"
        :text="is_text"
        :x-small="is_text"
        v-if="!is_text"
      >
        {{ title }}
      </v-btn>
      <a v-else v-on="on" dark class="white--text" v-bind="attrs">{{
        title
      }}</a>
    </template>
    <v-card>
      <v-card-title class="headline">{{ title }}</v-card-title>
      <v-card-text
        ><p class="text-caption" v-for="line in text" :key="line">
          {{ line }}
        </p></v-card-text
      >
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialog = false">Fechar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  usage_terms,
  privacy_policy,
  who_are_us,
} from "../assets/compliance_texts";
export default {
  name: "ComplianceTextButton",
  props: {
    is_text: Boolean,
    document: {
      validator: function(value) {
        return (
          ["usage_terms", "privacy_policy", "who_are_us"].indexOf(value) !== -1
        );
      },
    },
  },
  data: () => ({
    dialog: false,
    text: "",
    title: "",
  }),
  methods: {
    parseText(text) {
      return text.split("\n");
    },
  },
  mounted() {
    if (this.document == "usage_terms") {
      this.title = "Termos de uso";
      this.text = this.parseText(usage_terms);
    } else if (this.document == "privacy_policy") {
      this.title = "Política de Privacidade";
      this.text = this.parseText(privacy_policy);
    } else if (this.document == "who_are_us") {
      this.title = "Quem somos nós";
      this.text = this.parseText(who_are_us);
    } else {
      this.title = "Documento inválido";
      this.text = "Invalid document";
    }
  },
};
</script>

<style></style>
