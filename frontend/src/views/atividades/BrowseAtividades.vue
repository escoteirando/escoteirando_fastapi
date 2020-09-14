<template>
  <div>
    <FiltroAtividades v-on:do-filtro="doFiltro" />
  </div>
</template>

<script>
import FiltroAtividades from "./FiltroAtividades";
export default {
  components: { FiltroAtividades },
  methods: {
    doFiltro(filtro) {
      alert(JSON.stringify(filtro));
    },
  },
};
</script>
