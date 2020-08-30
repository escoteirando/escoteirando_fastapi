<template>
  <div class="NotFound">
    <v-container>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card height="400" color="transparent" flat>
            <div class="display-3 mt-5">Página não encontrada.</div>
            <div
              class="grey--text lighten-5"
            >A página que você está tentando acessar nunca existiu nessa realidade ou migrou para um universo paralelo.</div>
            <div class="paragraph-text mt-2">
              <br />
              <br />Tente voltar para a
              <router-link :to="{name:'home'}">página inicial</router-link>&nbsp;e repetir sua ação. Ou contate o suporte, se necessário.
            </div>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {};
</script>

<style>
.paragraph-text {
  font-size: 18px;
}
</style>