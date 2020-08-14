<template>
  <v-app-bar app color="primary" dark>
    <div class="d-flex align-center">
      <a href="/f">
        <v-img
          alt="Scouts Logo"
          class="shrink mr-2"
          contain
          :src="scout_logo"
          width="50"
      /></a>
      <h1 class="d-none d-lg-block">Escoteirando</h1>
    </div>

    <v-spacer></v-spacer>

    <v-btn
      @click="testClick"     
      text
    >
      <span class="mr-2">Test</span>
      <v-icon>mdi-open-in-new</v-icon>
    </v-btn>
    <v-menu bottom offset-y left open-on-hover v-if="isEnabledMenu">
      <template v-slot:activator="{ on, attrs }">
        <v-btn dark icon v-bind="attrs" v-on="on">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(item, i) in menu_items"
          :key="i"
          @click="menu_click(item)"
          ><v-list-item-icon v-if="item.icon"
            ><v-icon v-text="item.icon"
          /></v-list-item-icon>
          <v-list-item-title>{{ item.text }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data: () => ({
    scout_logo: require("../assets/scouts_white.svg"),
    menu_items: [
      { id: 1, text: "Menu text 1" },
      { id: 2, text: "Texto do menu 2" },
      { id: 3, text: "Sair", icon: "mdi-exit-to-app" },
    ],
  }),
  computed: {
    ...mapGetters("auth", ["isValid"]),
    isEnabledMenu() {
      return this.isValid && this.menu_items.length > 0;
    },
  },
  methods: {
    menu_click(item) {
      alert(item);
      console.log("Clicou", item);
    },
    testClick(){
       this.$swal("Teste")  
    }
  },
};
</script>

<style></style>
