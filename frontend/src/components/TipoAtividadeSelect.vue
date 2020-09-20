<template>
  <v-select
    v-model="tp_atividade"
    :items="items"
    item-value="id"
    item-text="text"
    prepend-icon="mdi-calendar-range"
    label="Tipo da atividade"
    v-on:change="changeTipo"
  />
</template>

<script>
import { getDictAsList } from "../api/dicionario";

export default {
  props: {
    tipo: {
      type: String,
      validator: (v) =>
        ["c", "e", "h", "i", "j", "m", "q"].indexOf(v.toLowerCase()) !== -1,
      default: () => "i",
    },
  },
  data: () => ({
    tp_atividade: null,
  }),
  computed: {
    items: () => getDictAsList("atividade"),
  },
  methods: {
    changeTipo(value) {
      this.$emit("changed", value);
    },
  },
  created() {
    this.tp_atividade = this.tipo;
  },
};
</script>

<style>
</style>