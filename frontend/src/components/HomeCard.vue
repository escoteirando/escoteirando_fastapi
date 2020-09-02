<template>
  <v-col sm="6" md="4" lg="3">
    <v-card>
      <v-card-title>{{card.title}}</v-card-title>
      <v-card-subtitle v-if="card.subtitle">{{card.subtitle}}</v-card-subtitle>
      <v-card-actions v-if="card.route">
        <v-btn color="primary" v-if="route" :to="route">Acessar</v-btn>
        <v-btn color="secondary" v-else :href="href" target="_new">Acessar</v-btn>
      </v-card-actions>
    </v-card>
  </v-col>
</template>

<script>
export default {
  props: {
    card: {
      type: Object,
      default: function () {
        return {
          title: null,
          route: null,
          subtitle: null,
          image: null,
          flex: 6,
        };
      },
    },
  },
  computed: {
    route() {
      return this.card.route && !this.card.route.startsWith("http")
        ? { name: this.card.route }
        : null;
    },
    href() {
      return this.card.route && this.card.route.startsWith("http")
        ? this.card.route
        : null;
    },    
  },
};
</script>
