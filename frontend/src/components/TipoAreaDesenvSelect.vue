<template>
  <v-select
    v-model="tp_area"
    :items="items"
    item-value="id"
    item-text="text"
    prepend-icon="mdi-star-circle"
    label="Área de Desenvolvimento"
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
        ["f", "i", "c", "a", "s", "e"].indexOf(v.toLowerCase()) !== -1,
      default: () => "f",
    },
  },
  computed: {
    items: () => getDictAsList("area"),
  },
  data: function () {
    return {
      tp_area: this.tipo.toLowerCase(),
    };
  },

  methods: {
    changeTipo(value) {
      this.$emit("changed", value);
    },
  },
};
</script>

<style>
</style>