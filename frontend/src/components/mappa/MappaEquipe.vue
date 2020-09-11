<template>
  <v-col sm="6" md="4" lg="3">
    <v-card class="mx-auto" :loading="loading">
      <v-card-title>Minha Equipe</v-card-title>
      <v-card-text v-if="!loading">
        <v-expansion-panels>
          <v-expansion-panel v-for="(item,i) in equipe" :key="i">
            <v-expansion-panel-header>{{item.nome}}</v-expansion-panel-header>
            <v-expansion-panel-content>
              <MappaListaAssociado :subsecao="item" :codigoTipoSecao="codigoTipoSecao" />
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import MappaListaAssociado from "./MappaListaAssociado";
export default {
  components: { MappaListaAssociado },
  data() {
    return {
      loading: true,
      nome_grupo: "NÃO IDENTIFICADO",
      codigoTipoSecao: 0,
      codigoSecao: 0,
      cod_grupo: 0,
      cod_regiao: "ZZ",
      equipe: [
        {
          codigo: 0,
          nome: "Matilha 1",
          codigoSecao: 0,
          codigoLider: 4,
          codigoViceLider: 1,
          associados: [
            {
              codigo: 1,
              nome: "Guionardo",
              dataNascimento: "1977-02-05T00:00:00.000Z",
              sexo: "M",
            },
            {
              codigo: 2,
              nome: "João",
              dataNascimento: "2008-12-31T00:00:00.000Z",
              sexo: "M",
            },
            {
              codigo: 3,
              nome: "Benjamin",
              dataNascimento: "2014-02-07T00:00:00.000Z",
              sexo: "M",
            },
            {
              tipo: 2,
              codigo: 4,
              nome: "Marines",
              dataNascimento: "1977-07-05T00:00:00.000Z",
              sexo: "F",
            },
          ],
        },
        {
          codigo: 0,
          nome: "Matilha 2",
          codigoSecao: 0,
          codigoLider: 0,
          codigoViceLider: 0,
          associados: [
            {
              codigo: 0,
              nome: null,
              dataNascimento: "2020-09-11T01:10:45.318Z",
              sexo: null,
            },
          ],
        },
      ],
    };
  },

  async mounted() {
    const secao = await this.API.MAPPA.getSecao();
    if (secao) {
      this.codigoTipoSecao = secao.codigoTipoSecao;
      this.codigoSecao = secao.codigo;
      this.equipe = await this.API.MAPPA.getEquipe(this.codigoSecao);
    }
    // const user_info = await this.API.MAPPA.getUserInfo();
    // if (user_info) {
    //   this.nome_grupo = user_info.nom_grupo;
    //   this.cod_grupo = user_info.cod_grupo;
    //   this.cod_regiao = user_info.cod_regiao;
    // }
    this.loading = false;
  },
};
</script>

<style>
</style>