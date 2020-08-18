<template>
  <div>
    <Atividade showRamo/>
  </div>
</template>

<script>
import Atividade from "../components/Atividade";
export default {
  components: { Atividade },
  data: () => ({
    dialog: false,
    text: "",
    title: "",
  }),
  methods: {
    changed(value) {
      console.log("Changed tipo to", value);
    },
  },
};
</script>

<style>
</style>