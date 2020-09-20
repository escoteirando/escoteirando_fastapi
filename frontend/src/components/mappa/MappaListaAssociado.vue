<template>
  <v-list dense>
    <v-list-item v-for="(item,i) in associados" :key="i">
      <v-list-item-content>
        <v-list-item-title v-text="item.nome" />
        <v-list-item-subtitle v-text="item.descricao" />
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
import { idadeAsString } from "../../api/tools";
import { getDict } from "../../api/dicionario";
export default {
  data: function () {
    return {
      associados: [
        {
          tipo: 1,
          codigo: 1,
          nome: "Guionardo",
          dataNascimento: "1977-02-05T00:00:00.000Z",
          sexo: "M",
        },
        {
          tipo: 0,
          codigo: 2,
          nome: "João",
          dataNascimento: "2008-12-31T00:00:00.000Z",
          sexo: "M",
        },
        {
          tipo: 1,
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
    };
  },
  props: {
    subsecao: Object,
    codigoTipoSecao: Number,

    // codigoLider: 0,
    // codigoViceLider: 0,
    // associados: [
    //   {
    //     codigo: 0,
    //     nome: null,
    //     dataNascimento: "2020-09-11T01:10:45.318Z",
    //     sexo: null,
    //   },
    // ],
  },
  methods: {
    getDescricao(associado, tipo) {
      return (
        getDict("membro_equipe", this.codigoTipoSecao)[tipo][associado.sexo] +        
        " " +
        idadeAsString(associado.dataNascimento)
      );
    },
    getTipo(associado) {
      switch (associado.codigo) {
        case this.subsecao.codigoLider:
          return 1;
        case this.subsecao.codigoViceLider:
          return 2;
      }
      return 0;
    },
  },
  mounted() {
    let i = 0;
    let associados = [];
    let associado = null;
    let lider = null;
    let viceLider = null;
    let tipo = 0;
    for (i = 0; i < this.subsecao.associados.length; i++) {
      associado = this.subsecao.associados[i];
      tipo = this.getTipo(associado);
      associado = {
        tipo: tipo,
        descricao: this.getDescricao(associado, tipo),
        ...associado,
      };

      switch (tipo) {
        case 1:
          lider = associado;
          break;
        case 2:
          viceLider = associado;
          break;
        default:
          associados.push({ tipo: 0, ...associado });
      }
    }
    associados = associados.sort((a, b) =>
      a.dataNascimento > b.dataNascimento
        ? 1
        : b.dataNascimento > a.dataNascimento
        ? -1
        : 0
    );
    if (lider) {
      associados.unshift(lider);
    }
    if (viceLider) {
      associados.push(viceLider);
    }
    this.associados = associados;
  },
};
</script>

<style>
</style>