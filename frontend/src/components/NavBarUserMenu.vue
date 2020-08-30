<template>
  <v-menu bottom offset-y left open-on-hover v-if="isEnabledMenu">
    <template v-slot:activator="{ on, attrs }">
      <v-btn dark icon v-bind="attrs" v-on="on">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </template>

    <v-list>
      <v-list-item v-for="(item, i) in getNavMenu" :key="i" @click="menu_click(item)">
        <v-list-item-icon v-if="item.icon">
          <v-icon v-text="item.icon" />
        </v-list-item-icon>
        <v-list-item-title>{{ item.text }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  data: () => ({
    menu_items: [
      { id: 1, text: "Menu text 1" },
      { id: 2, text: "Texto do menu 2" },
      { id: 3, text: "Sair", icon: "mdi-exit-to-app", action: "logout" },
    ],
  }),
  computed: {
    ...mapGetters("backend", ["isLoggedUser"]),
    ...mapGetters("user_menus", ["getNavMenu"]),
    isEnabledMenu() {
      return this.isLoggedUser && this.getNavMenu.length > 0;
    },
  },
  methods: {
    ...mapActions("user_menus", ["callAction"]),
    menu_click(item) {
      this.callAction(item.id);     
    },
    load_menus() {
      if (!this.isEnabledMenu) {
        return;
      }
      window.axios
        .get("/api/user/menu")
        .then(function (result) {
          this.menu_items = result;
        })
        .catch((error) => console.error("[USER MENU]", error));
    },
  },
  mounted() {
    this.load_menus();
  },
};
</script>

<style>
</style>