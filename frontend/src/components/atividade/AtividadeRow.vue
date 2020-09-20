<template>
  <v-card>
    <v-card-title>{{nome}}</v-card-title>
    <v-divider />
    <v-list dense>
      <v-list-item v-for="item in items" :key="item.name">
        <v-list-item-content>{{item.name}}</v-list-item-content>
        <v-list-item-content :class="item.right?'align-end':''">{{item.value}}</v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import { getDict } from "../../api/dicionario";
export default {
  props: ["atividade"],
  data: function () {
    return {
      items: [],
      ramo: null,
      nome: null,
      atv: {
        tp_ramo: this.ramo,
        area: null,
        tipo: null,
        dur_min: 5,
        dur_max: 10,
        duracao: [5, 20],
        slider: 40,
        descricao: null,
        como_avaliar: null,
        restricoes: [],
        progressoes: [],
      },
    };
  },
  mounted() {
    this.items = [
      {
        name: "Ramo",
        value: getDict("ramo", this.atividade.tp_ramo).text,
        right: false,
      },
      {
        name: "Área",
        value: getDict("area", this.atividade.area).text,
        right: false,
      },
      {
        name: "Duração",
        value: `${this.atividade.dur_min} a ${this.atividade.dur_max} min`,
        right: false,
      },
      {
        name: "Tipo",
        value: getDict("atividade", this.atividade.tipo).text,
        right: false,
      },
    ];
    this.nome = this.atividade.nome;
  },
};
</script>

<style>
</style>