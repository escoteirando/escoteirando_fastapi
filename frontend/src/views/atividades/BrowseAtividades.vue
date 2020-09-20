<template>
  <div>
    <FiltroAtividades v-on:do-filtro="doFiltro" />
    <v-data-iterator :items="items" :items-per-page.sync="itemsPerPage" hide-default-footer>
      <template v-slot:header>
        <v-toolbar class="mb-2" dark flat>
          <v-toolbar-title>Atividades</v-toolbar-title>
        </v-toolbar>
      </template>
      <template v-slot:default="props">
        <v-row>
          <v-col v-for="item in props.items" :key="item.name" cols="12" sm="6" md="4" lg="3">
            <AtividadeRow :atividade="item" />
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </div>
</template>

<script>
import FiltroAtividades from "./FiltroAtividades";
import AtividadeRow from "../../components/atividade/AtividadeRow";
export default {
  components: { FiltroAtividades, AtividadeRow },
  data() {
    return {
      itemsPerPage: 16,
      items: [
        {
          tp_ramo: 1,
          nome: "Caça-lobinho",
          area: "f",
          dur_min: 15,
          dur_max: 25,
          tipo: "j",
        },
        {
          tp_ramo: 2,
          nome: "Nós: direito e escota",
          area: "i",
          dur_min: 10,
          dur_max: 20,
          tipo: "e",
        },
        {
          tp_ramo: 3,
          nome: "Culto",
          area: "e",
          dur_min: 10,
          dur_max: 15,
          tipo: "c",
        },
        {
          tp_ramo: 4,
          nome: "Pedágio",
          area: "s",
          dur_min: 120,
          dur_max: 120,
          tipo: "o",
        },
        {
          tp_ramo: 1,
          nome: "As caçadas de Kaa",
          area: "s",
          dur_min: 120,
          dur_max: 120,
          tipo: "h",
        },
      ],
    };
  },
  methods: {
    doFiltro(filtro) {
      alert(JSON.stringify(filtro));
    },
  },
};
</script>
