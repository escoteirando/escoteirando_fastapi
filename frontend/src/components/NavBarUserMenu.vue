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
    ...mapGetters("user_menus", ["getNavMenu"]),
    isEnabledMenu() {
      return this.API.USER.isLogged(); //&& this.getNavMenu.length > 0;
    },
  },
  methods: {
    ...mapActions("user_menus", [
      "callAction",
      "load_user_menus",
      "load_user_cards",
    ]),
    menu_click(item) {
      this.callAction(item.id);
    },
    async loadMenus() {
      let menus = await this.API.USER.getUserMenus();
      if (!menus) {
        menus = [];
      }
      let cards = await this.API.USER.getUserCards();
      if (cards) {
        let id = 600;
        cards.forEach((x) => menus.push({ id: id++, text: x.title }));
      }
      console.log("[NAVBAR] MENUS", menus);
      this.menu_items = menus;
    },
  },
  mounted() {
    this.loadMenus();
  },
};
</script>

<style>
</style>