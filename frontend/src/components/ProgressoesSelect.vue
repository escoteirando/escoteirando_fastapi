<template>
  <v-select
    v-model="opcoes"
    :items="progressoes"
    item-text="text"
    item-value="cod"
    label="Progressões"
    multiple
    chips
    deletable-chips
    counter
    :loading="loading"
    no-data-text="Informe as progressões para esta atividade"
  />
</template>

<script>
import { getDict } from "../api/dicionario";
export default {
  props: ["ramo"],
  data() {
    return {
      loading: true,
      opcoes: [],
      ramo_progs: null,
      progressoes: {},
    };
  },
  async created() {
    if (!getDict("ramo", this.ramo)) {
      console.error("[ProgressoesSelect] RAMO INVÁLIDO", this.ramo);
    } else {
      this.progressoes = this.parserProgressao(
        await this.API.MAPPA.getProgressoes(this.ramo)
      );
      console.log("[ProgressoesSelect] CREATED");
    }
    this.loading = false;
  },
  methods: {
    parserProgressao(progressoes) {
      if (!progressoes) {
        return [];
      }
      const result = progressoes.map((x) => ({
        cod: x.codigo,
        text: `${x.codigoUeb} ${x.descricao} [${x.areaDesenvolvimento}]`,
      }));
      return result;
    },
  },
  computed: {
    lista_progressoes() {
      if (!getDict("ramo", this.ramo)) {
        console.error("[ProgressoesSelect] RAMO INVÁLIDO", this.ramo);
        return [];
      }

      return this.progressoes[this.ramo];
    },
  },
};
</script>

<style>
</style>