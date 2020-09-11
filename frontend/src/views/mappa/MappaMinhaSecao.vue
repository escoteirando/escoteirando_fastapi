<template>
  <v-container fluid>
    <v-row dense>
      <MappaGrupo />
      <MappaSecao />
      <MappaEquipe />
      <MappaProgressaoSecao />
    </v-row>
  </v-container>
</template>

<script>
import MappaGrupo from "../../components/mappa/MappaGrupo";
import MappaSecao from "../../components/mappa/MappaSecao";
import MappaEquipe from "../../components/mappa/MappaEquipe";
import MappaProgressaoSecao from "../../components/mappa/MappaProgressaoSecao";
export default {
  components: { MappaGrupo, MappaSecao, MappaEquipe, MappaProgressaoSecao },
};
</script>

<style>
</style>