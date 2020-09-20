<template>
  <v-toolbar :title="descricao">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon color="primary" dark v-bind="attrs" v-on="on">
          <v-icon>mdi-filter</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Filtro</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  :items="areas"
                  label="Área de desenvolvimento"
                  v-model="filtro.area"
                  item-text="text"
                  item-value="id"
                  dense
                />
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  :items="tipos"
                  label="Tipo de atividade"
                  v-model="filtro.tipo"
                  item-text="text"
                  item-value="id"
                  dense
                />
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  :items="ramos"
                  label="Ramo"
                  v-model="filtro.ramo"
                  item-text="text"
                  item-value="id"
                  dense
                />
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Palavras-chave" v-model="filtro.palavras_chave"></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="resetFiltros()">Cancelar</v-btn>
          <v-btn color="blue darken-1" text @click="filtrar()">Filtrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-toolbar-title>Filtro:</v-toolbar-title>
    &nbsp;{{descricao}}
    <v-divider />
    <v-btn icon @click="doFiltro">
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
import { getDictAsList, getDict } from "../../api/dicionario";
export default {
  data() {
    return {
      filtro: { area: null, tipo: null, ramo: null, palavras_chave: null },
      ultimoFiltro: {
        area: null,
        tipo: null,
        ramo: null,
        palavras_chave: null,
      },
      areas: [],
      tipos: [],
      ramos: [],
      dialog: false,
    };
  },
  computed: {
    descricao() {
      let desc = [];
      if (this.filtro.area) {
        desc.push("Área: " + getDict("area", this.filtro.area).text);
      }
      if (this.filtro.tipo) {
        desc.push("Tipo: " + getDict("atividade", this.filtro.tipo).text);
      }
      if (this.filtro.ramo) {
        desc.push("Ramo: " + getDict("ramo", this.filtro.ramo).text);
      }
      if (this.filtro.palavras_chave) {
        desc.push("Palavras-chave: " + this.filtro.palavras_chave);
      }

      if (desc.length == 0) {
        desc.push("Sem filtro");
      }
      return desc.join(", ");
    },
  },
  mounted() {
    this.areas = getDictAsList("area");
    this.areas.unshift({ id: null, text: "Todas" });
    this.tipos = getDictAsList("atividade");
    this.tipos.unshift({ id: null, text: "Todos" });
    this.ramos = getDictAsList("ramo");
    this.ramos.unshift({ id: null, text: "Todos" });
  },
  methods: {
    filtrar() {
      this.ultimoFiltro = this.filtro;
      this.dialog = false;
    },
    resetFiltros() {
      this.filtro = this.ultimoFiltro;
      this.dialog = false;
    },
    doFiltro() {
      console.log("do-filtro", this.filtro);
      this.$emit("do-filtro", this.filtro);
    },
  },
};
</script>

<style>
</style>