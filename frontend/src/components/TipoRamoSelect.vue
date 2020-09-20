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
import { getDictAsList } from "../api/dicionario";
export default {
  props: { tipo: String },
  data: () => ({
    tp_ramo: null,
  }),
  computed: {
    items: () => getDictAsList("ramo"),
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