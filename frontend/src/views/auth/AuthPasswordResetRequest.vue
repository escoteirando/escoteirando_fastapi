<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Redefinir senha</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              id="user"
              label="Usuário/e-mail"
              name="user"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
            />

            
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text small to="login">Login</v-btn>          
          <v-spacer></v-spacer>
          <v-btn color="primary">Enviar link</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    username: "",
    password: "",
  }),
};
</script>

<style></style>
