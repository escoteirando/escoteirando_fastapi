<template>
  <v-text-field
    id="password"
    label="Senha"
    name="password"
    :color="textClass"
    :counter="20"
    prepend-icon="mdi-lock"
    :append-icon="visibility ? 'mdi-eye' : 'mdi-eye-off'"
    :type="visibility ? 'text' : 'password'"
    v-model="password"
    v-on:blur="handleExit"
    @click:append="() => (visibility = !visibility)"
    :rules="passwordRules"
    required
    :hint="hint"
    v-on:change="passwordLevel"
  />
</template>

<script>
import { passwordNeeds, passwordRules } from "../api/tools";
export default {
  data() {
    return {
      textClass: "",
      password: "",
      visibility: false,
      passwordRules: passwordRules,
      messages: [],
      hint: "",
    };
  },
  methods: {
    handleExit() {
      this.$emit("password", this.password);
    },
    passwordLevel() {
      let msg = passwordNeeds(this.password);
      let level = 5 - msg.length;
      this.hint = msg.join(", ");
      return level;
    },
  },
};
</script>

<style></style>
