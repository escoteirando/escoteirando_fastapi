<template>
  <v-container fluid>
    <v-row dense>
      <MappaGrupo />
      <MappaSecao />
      <MappaEquipe />
    </v-row>
  </v-container>
</template>

<script>
import MappaGrupo from "../../components/mappa/MappaGrupo";
import MappaSecao from "../../components/mappa/MappaSecao";
import MappaEquipe from "../../components/mappa/MappaEquipe";
export default {
  components: { MappaGrupo, MappaSecao, MappaEquipe },
};
</script>

<style>
</style>