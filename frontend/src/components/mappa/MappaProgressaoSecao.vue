<template>
  <v-col sm="12" md="8" lg="6">
    <v-card class="mx-auto" :loading="loading">
      <v-card-title>Progressão da Seção</v-card-title>
      <v-card-text v-if="!loading">
        <v-select :items="anos" v-model="ano" @change="changedAno" label="Ano" />
        <br />
        <MappaProgressaoChart v-if="!loading" :chart-data="datacollection" ref="chart" />
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import MappaProgressaoChart from "./MappaProgressaoChart";
import { dateAsString } from "../../api/tools";
export default {
  components: { MappaProgressaoChart },
  data() {
    return {
      datacollection: null,
      loading: true,
      progressoesPorAno: {},
      anos: [],
      ano: null,
      progressoes: null,
    };
  },
  async mounted() {
    const secao = await this.API.MAPPA.getSecao();
    if (secao) {
      this.progressoes = await this.API.MAPPA.getProgressoesSecao(secao.codigo);
      console.log("PROGRESSOES", this.progressoes);
      this.selecionarAnos();
      this.changedAno();
    }
    this.loading = false;
  },
  methods: {
    selecionarAnos() {
      let ano;
      let anos = {};
      this.progressoes.forEach(function (progressao) {
        ano = progressao.data.substring(0, 4);
        anos[ano] = true;
      });

      this.anos = Object.keys(anos);
      this.ano = ano;
    },
    changedAno() {
      console.log("Carregando Progressoes Ano", this.ano);
      this.loading = true;
      this.fillData(this.ano);
      this.loading = false;
    },
    fillData(ano) {
      let ind = 0;
      let labels = [];
      let f = [];
      let i = [];
      let c = [];
      let a = [];
      let s = [];
      let e = [];
      for (ind = 0; ind < this.progressoes.length; ind++) {
        const progressao = this.progressoes[ind];
        if (progressao.data.substring(0, 4) != ano) {
          continue;
        }
        labels.push(dateAsString(new Date(progressao.data)).substring(3, 10));
        f.push(progressao.f);
        i.push(progressao.i);
        c.push(progressao.c);
        a.push(progressao.a);
        s.push(progressao.s);
        e.push(progressao.e);
      }

      this.datacollection = {
        labels: labels,
        datasets: [
          {
            label: "Físico",
            backgroundColor: "#008000",
            data: f,
            fill: false,
          },
          {
            label: "Intelectual",
            backgroundColor: "#000080",
            data: i,
            fill: false,
          },
          {
            label: "Caráter",
            backgroundColor: "#ff6600",
            data: c,
            fill: false,
          },
          {
            label: "Afetivo",
            backgroundColor: "#800080",
            data: a,
            fill: false,
          },
          {
            label: "Social",
            backgroundColor: "#008080",
            data: s,
            fill: false,
          },
          {
            label: "Espiritual",
            backgroundColor: "#550000",
            data: e,
            fill: false,
          },
        ],
      };
      console.log("Ano Selecionado", this.datacollection);
    },
  },
};
</script>

<style>
</style>