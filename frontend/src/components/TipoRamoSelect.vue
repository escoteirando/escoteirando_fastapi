<template>
  <v-select
    v-model="tp_ramo"
    :items="items"
    item-value="id"
    item-text="text"
    prepend-icon="mdi-leaf"
    label="Ramo"
    v-on:change="changeTipo"
  />
</template>

<script>
import { tipos_ramos } from "../api/consts";
export default {
  props: { tipo: String },
  data: () => ({
    tp_ramo: null,
  }),
  computed: {
    items: () => tipos_ramos,
  },
  methods: {
    changeTipo(value) {
      this.$emit("changed", value);
    },
  },
  created() {
    this.tp_ramo = this.tipo;
  },
};
</script>

<style>
</style>