<template>
  <v-card>
    <v-card-title>Atividade</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-if="showRamo">
          <TipoRamoSelect :ramo="ramo" v-on:changed="changedRamo" />
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <TipoAtividadeSelect v-on:changed="changedTipoAtividade" />
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <v-label class="pl-0">Duração: {{duracao[0]}} a {{duracao[1]}} min</v-label>

          <v-range-slider
            v-model="duracao"
            thumb-label
            :max="120"
            :min="0"
            hide-details
            step="5"
            ticks
            class="align-center"
          ></v-range-slider>
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <v-text-field v-model="nome" label="Nome" prepend-icon="mdi-rename-box" />
        </v-col>
        <v-col cols="12" sm="6" md="4" v-if="ehAtividadeEducativa">
          <v-textarea
            v-model="descricao"
            class="mx-2"
            label="Descrição"
            rows="1"
            prepend-icon="mdi-comment"
          ></v-textarea>
        </v-col>
        <v-col cols="12" sm="6" md="4" v-if="ehAtividadeEducativa">
          <v-textarea
            v-model="como_avaliar"
            class="mx-2"
            label="Como Avaliar"
            rows="1"
            prepend-icon="mdi-comment"
          ></v-textarea>
        </v-col>
        <v-col v-if="ehAtividadeEducativa">
          <TipoAreaDesenvSelect v-on:changed="changedAreaDesenv" />
        </v-col>
        <v-col v-if="ehAtividadeEducativa && tp_ramo">
          <ProgressoesSelect :ramo="tp_ramo" :key="tp_ramo" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import TipoAtividadeSelect from "./TipoAtividadeSelect";
import TipoRamoSelect from "./TipoRamoSelect";
import TipoAreaDesenvSelect from "./TipoAreaDesenvSelect";
import ProgressoesSelect from "./ProgressoesSelect";

import { getDict } from "../api/dicionario";

export default {
  components: {
    TipoAtividadeSelect,
    TipoRamoSelect,
    TipoAreaDesenvSelect,
    ProgressoesSelect,
  },
  props: {
    ramo: {
      type: String,
      validator: (v) => ["A", "E", "S", "C"].indexOf(v) !== -1,
    },
    showRamo: Boolean,
  },

  data: function () {
    return {
      tp_ramo: this.ramo,
      area: null,
      tipo: null,
      dur_min: 5,
      dur_max: 10,
      duracao: [5, 20],
      slider: 40,
      nome: null,
      descricao: null,
      como_avaliar: null,
      restricoes: [],
      progressoes: [],
      key_ps: 0,
    };
  },
  computed: {
    ehAtividadeEducativa() {
      return getDict("atividade", this.tipo || 1).educ;
    },
  },
  methods: {
    changedTipoAtividade(value) {
      this.tipo = value;
    },
    changedRamo(value) {
      this.tp_ramo = value;
    },
    changedAreaDesenv(value) {
      this.area = value;
    },
  },
  created() {},
};
</script>

<style>
</style>