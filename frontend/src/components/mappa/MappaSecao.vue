<template>
  <v-col sm="6" md="4" lg="3">
    <v-card class="mx-auto" :loading="loading">
      <v-card-title>Minha seção</v-card-title>
      <v-card-text v-if="!loading">{{secao.nome}}</v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      secao: null,
    };
  },

  async mounted() {
    const secao = await this.API.MAPPA.getSecao();
    if (secao) {
      this.secao = secao;
    }
    this.loading = false;
  },
};
</script>

<style>
</style>