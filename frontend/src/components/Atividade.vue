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
        <v-col cols="6" sm="3" md="2">
          <v-text-field
            v-model="dur_min"
            type="number"
            label="Duração mínima"
            prepend-icon="mdi-clock-in"
          />
        </v-col>
        <v-col cols="6" sm="3" md="2">
          <v-text-field
            v-model="dur_max"
            type="number"
            label="Duração máxima"
            prepend-icon="mdi-clock-out"
          />
        </v-col>
        <v-col cols="12" sm="6" md="4" v-if="ehAtividadeEducativa">
          <v-text-field v-model="nome" label="Nome" />
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
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>

import TipoAtividadeSelect from "./TipoAtividadeSelect";
import TipoRamoSelect from "./TipoRamoSelect";
import TipoAreaDesenvSelect from "./TipoAreaDesenvSelect";
import { tipos_atividade_educativos } from "../api/consts";
export default {
  components: { TipoAtividadeSelect, TipoRamoSelect, TipoAreaDesenvSelect },
  props: {
    ramo: {
      type: String,
      validator: (v) => ["A", "T", "S", "C"].indexOf(v) !== -1,
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
      nome: null,
      descricao: null,
      como_avaliar: null,
      restricoes: [],
      progressoes: [],
    };
  },
  computed: {
    ehAtividadeEducativa() {
      return tipos_atividade_educativos.indexOf(this.tipo) !== -1;
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
  created() {
   
  },
};
</script>

<style>
</style>