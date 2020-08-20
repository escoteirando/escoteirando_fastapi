<template>
  <v-select
    v-model="progressoes"
    :items="lista_progressoes"
    item-text="text"
    item-value="cod"
    label="Progressões"
    multiple
    chips
  />
</template>

<script>
export default {
  data() {
    return {
      progressoes: [],
      lista_progressoes: [
        { cod: "S1", text: "Progressão S1" },
        { cod: "S2", text: "Progressão S2" },
      ],
    };
  },
  created() {
    for (let i = 0; i < 100; i++) {
      this.lista_progressoes.push({ cod: "P" + i, text: "Progressão P" + i });
    }
  },
};
</script>

<style>
</style>