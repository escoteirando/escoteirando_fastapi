<template>
  <div>
    <h1>Teste Home</h1>
    <a :href="swagger" target="empty">Swagger</a>
    <p>{{ getUser }}</p>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("backend", ["getUser", "getHost"]),
    swagger() {
      return this.getHost + "/docs";
    },
  },
};
</script>

<style></style>
