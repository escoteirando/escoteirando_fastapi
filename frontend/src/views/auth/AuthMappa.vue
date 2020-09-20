<template>
  <v-stepper v-model="e1">
    <v-stepper-header>
      <v-stepper-step :complete="e1 > 1" step="1">Você é um escotista?</v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="e1 > 2" step="2">Acesso ao mAPPa</v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="e1 > 3" step="3">Dados do escotista</v-stepper-step>
      <v-divider />
      <v-stepper-step :complete="e1 > 4" step="4">Seção(ões)</v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step step="5">Fim</v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-card class="mb-12" color="grey lighten-1" height="200px">
          <v-card-title>Recurso exclusivo para escotistas registrados na União dos Escoteiros do Brasil</v-card-title>

          <v-card-text>
            Nosso sistema permite que você tenha um acesso mais amigável aos dados da sua seção, que são registrados pelo aplicativo mAPPa Adulto.
            <br />Para tanto, será necessário que você informe suas credenciais utilizadas no mAPPa Adulto.
            <br />
            <strong>Garantimos que sua senha não será armazenada,</strong> pois o sistema de autenticação é baseado em chaves temporárias.
            <br />Sua senha será utilizada apenas para o acesso e descartada em seguida.
            <br />Para mais informações, consulte nosso Termo de Uso e a Política de Privacidade (links no rodapé do site).
          </v-card-text>
        </v-card>
        <v-btn color="primary" @click="e1=2">Continuar</v-btn>

        <v-btn text @click="naoQueroAgora">Não quero fazer isso agora</v-btn>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-card class="mb-12" color="grey lighten-1" height="200px">
          <v-card-title>Informe suas credenciais do mAPPa</v-card-title>
          <v-card-text>
            <v-form v-model="mappaValid">
              <v-container>
                <v-row>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="mappa.username"
                      label="Usuário mAPPa"
                      :rules="userRules"
                      required
                    />
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="mappa.password"
                      label="Senha do aplicativo mAPPa"
                      :rules="passRules"
                      required
                      type="password"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-card-text>
        </v-card>
        <v-alert prominent type="error" v-if="erroLogin" dismissible close-text="Fechar">
          <v-row align="center">
            <v-col class="grow">{{erroLogin}}</v-col>
          </v-row>
        </v-alert>

        <v-btn color="primary" :disabled="!mappaValid" @click="validarMAPPA">Continuar</v-btn>

        <v-btn text @click="naoQueroAgora">Não quero fazer isso agora</v-btn>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-card class="mb-12" color="grey lighten-1" height="200px">
          <v-form readonly>
            <v-container>
              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field v-model="user.nome" label="Nome" />
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field v-model="user.grupo" label="Grupo Escoteiro" />
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field v-model="user.nascimento" label="Data de nascimento" />
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card>

        <v-btn color="secondary" :disabled="!mappaLoginOk" @click="obterSecoes">Obter Seções</v-btn>
      </v-stepper-content>

      <v-stepper-content step="4">
        <v-card class="mb-12" color="grey lighten-1" height="200px">
          <v-container>
            <v-row>
              <v-col cols="12" md="4">
                <v-list-item two-line v-for="item in secoes" :key="item.codigo">
                  <v-list-item-icon>
                    <v-img contain height="84" :src="item.img" />
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{item.nome}}</v-list-item-title>
                    <v-list-item-subtitle>{{item.tipo}}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </v-container>
        </v-card>

        <v-btn color="primary" @click="finalizar">Finalizar</v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>
import store from "../../store";
import { dateAsString } from "../../api/tools";
import router from "@/router";
import { mapGetters } from "vuex";
import { getDict } from "../../api/dicionario";
export default {
  data() {
    return {
      e1: 1,
      mappa: { username: null, password: null },
      mappaValid: false,
      userRules: [(v) => !!v || "Usuário mAPPa é requerido"],
      passRules: [(v) => !!v || "Senha mAPPA é requerida"],
      erroLogin: "",
      mappaLoginOk: false,
      secoes: [],
    };
  },
  computed: {
    ...mapGetters("mappa", ["getMappa"]),
    user() {
      return {
        nome: this.getMappa.nome_completo,
        grupo:
          this.getMappa.cod_grupo +
          "/" +
          this.getMappa.cod_regiao +
          " " +
          this.getMappa.nom_grupo,
        modalidade: [
          "Alcatéia",
          "Tropa Escoteira",
          "Tropa Sênior",
          "Clã Pioneiro",
        ],
        sexo: this.getMappa.sexo,
        nascimento: dateAsString(this.getMappa.nascimento),
      };
    },
    secoesStr() {
      return this.getSecoes.map((x) => x.tipo + ": " + x.nome).join(", ");
    },
  },
  mounted() {
    console.log("[VIEW AuthMappa] MOUNTED");
  },
  methods: {
    validarMAPPA() {
      this.erroLogin = "";
      window.axios
        .post("/api/mappa/login", {
          username: this.mappa.username,
          password: this.mappa.password,
        })
        .then((response) => {
          console.log("MAPPA LOGIN", response);
          store.dispatch("mappa/setMappa", response.data);
          this.mappaLoginOk = true;

          this.e1 = 3;
        })
        .catch((error) => {
          console.error("MAPPA LOGIN", error);
          this.erroLogin = error.data;
        });
    },
    naoQueroAgora() {
      this.$fire({
        title: "Acesso aos dados do mAPPa",
        icon: "question",
        text:
          'Se você não quiser informar suas credenciais do mAPPa agora, poderá fazê-lo acessando o menu "Credenciais mAPPa" do seu usuário.',
        showCancelButton: true,
        confirmButtonText: "Informarei em outra hora",
        cancelButtonText: "Voltar",
      }).then((result) => {
        if (!result.value) {
          return;
        }
        const data = {
          user_id: -1,
          authentication: "",
          user_name: "",
          auth_valid_until: 0,
          sexo: "",
          nascimento: "",
          ueb_id: -1,
        };

        window.axios.post("/api/mappa/save", data).then((response) => {
          console.log("[MAPPA] NÃO REGISTROU", response);
          router.push({ name: "home" });
        });
      });
    },
    finalizar() {
      const data = {
        user_id: this.getMappa.user_id,
        authentication: this.getMappa.authorization,
        user_name: this.mappa.username,
        auth_valid_until: this.getMappa.auth_valid_until,
        sexo: this.getMappa.sexo,
        nascimento: this.getMappa.nascimento.toISOString(),
        ueb_id: this.getMappa.user_id,
      };
      console.log("[MAPPA] FINALIZAR", data);
      window.axios.post("/api/mappa/save", data).then((response) => {
        console.log("[MAPPA] ATUALIZOU", response.data);
        router.push({ name: "home" });
        router.go();
      });
    },
    obterSecoes() {
      let data = {
        user_id: this.getMappa.user_id,
        authentication: this.getMappa.authorization,
        username: this.mappa.username,
        auth_valid_until: this.getMappa.auth_valid_until,
      };

      console.log("[MAPPA SECOES] OBTER SECOES", data);
      this.API.MAPPA.getSecoes()
        .then((data) => {
          console.log("[MAPPA SECOES]", data);
          let secoes = [];
          for (let i = 0; i < data.length; i++) {
            const ramo = getDict("ramo", data[i].codigoTipoSecao);
            secoes.push({
              img: ramo.logo,
              codigo: data[i].codigo,
              nome: data[i].nome,
              tipo: ramo.text,
            });
          }

          this.secoes = secoes;
          this.e1 = 4;
        })
        .catch((error) => {
          console.error("[MAPPA SECOES]", error);
        });
    },
  },
};
</script>

<style>
</style>