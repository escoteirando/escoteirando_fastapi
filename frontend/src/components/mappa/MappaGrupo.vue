<template>
  <v-col sm="6" md="4" lg="3">
    <v-card class="mx-auto" :loading="loading">
      <v-card-title>Meu grupo</v-card-title>
      <v-card-text v-if="!loading">{{cod_grupo}}/{{cod_regiao}} {{nome_grupo}}</v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      nome_grupo: "NÃO IDENTIFICADO",
      cod_grupo: 0,
      cod_regiao: "ZZ",
    };
  },

  async mounted() {
    const user_info = await this.API.MAPPA.getUserInfo();
    if (user_info) {
      this.nome_grupo = user_info.nom_grupo;
      this.cod_grupo = user_info.cod_grupo;
      this.cod_regiao = user_info.cod_regiao;
    }
    this.loading = false;
  },
};
</script>

<style>
</style>