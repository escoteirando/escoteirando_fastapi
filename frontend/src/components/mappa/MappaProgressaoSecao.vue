<template>
  <v-col sm="12" md="8" lg="6">
    <v-card class="mx-auto" :loading="loading">
      <v-card-title>Progressão da Seção</v-card-title>
      <v-card-text v-if="!loading">
        <MappaProgressaoChart :chartdata="datacollection" />
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
    return { datacollection: null, codigoSecao: 0, loading: true };
  },
  async mounted() {
    const secao = await this.API.MAPPA.getSecao();
    if (secao) {
      this.codigoTipoSecao = secao.codigoTipoSecao;
      this.codigoSecao = secao.codigo;
      let progressoes = await this.API.MAPPA.getProgressoesSecao(
        this.codigoSecao
      );
      this.fillData(progressoes);
    }
    this.loading = false;
  },
  methods: {
    fillData(progressoes) {
      let ind = 0;
      let labels = [];
      let f = [];
      let i = [];
      let c = [];
      let a = [];
      let s = [];
      let e = [];
      for (ind = 0; ind < progressoes.length; ind++) {
        labels.push(
          dateAsString(new Date(progressoes[ind].data)).substring(3, 10)
        );
        f.push(progressoes[ind].f);
        i.push(progressoes[ind].i);
        c.push(progressoes[ind].c);
        a.push(progressoes[ind].a);
        s.push(progressoes[ind].s);
        e.push(progressoes[ind].e);
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
    },
  },
};
</script>

<style>
</style>