<template>
  <v-menu bottom offset-y left open-on-hover>
    <template v-slot:activator="{ on, attrs }">
      <v-btn dark icon v-bind="attrs" v-on="on">
        <v-icon>mdi-circle</v-icon>
      </v-btn>
    </template>

    <v-list>
      <v-list-item v-for="(item, i) in menu_items" :key="i">
        <v-list-item-title>{{ item.text }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data: () => ({}),
  computed: {
    ...mapGetters("backend", ["getUser"]),
    menu_items() {
      let i = [];
      i.push({ id: 1, text: `Usuario: ${this.getUser.full_name}` });
      return i;
    },
  },
};
</script>

<style>
</style>