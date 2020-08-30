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
            <strong>Garantimos que sua senha não será armazenada,</strong> pois o sistema de autenticação é baseado em chaves temporárias. Sua senha será utilizada apenas para o acesso e descartada em seguida.
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
                  <v-text-field v-model="user.data_nascimento" label="Data de nascimento" />
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
    ...mapGetters("mappa", ["getMappa", "getSecoes"]),
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
        data_nascimento: dateAsString(this.getMappa.data_nascimento),
      };
    },
    secoesStr() {
      return this.getSecoes.map((x) => x.tipo + ": " + x.nome).join(", ");
    },
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
          data_nascimento: "",
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
        user_id: -1,
        authentication: "",
        user_name: "",
        auth_valid_until: 0,
        sexo: "",
        data_nascimento: "",
        ueb_id: -1,
      };
      console.log("[MAPPA] FINALIZAR", data);
    },
    obterSecoes() {
      let data = {
        user_id: this.getMappa.user_id,
        authentication: this.getMappa.authorization,
        username: this.mappa.username,
        auth_valid_until: this.getMappa.auth_valid_until,
      };
      window.axios
        .post("/api/mappa/secoes", data)
        .then((resp_sec) => {
          console.log("MAPPA SECOES", resp_sec);
          resp_sec.data.forEach((item) => {
            return {
              img: this.getSecaoImg(item.tipo),
              codigo: item.codigo,
              nome: item.nome,
              tipo: item.tipo,
            };
          });
          this.secoes = resp_sec.data;
          store.dispatch("mappa/setSecoes", resp_sec.data);
          this.e1 = 4;
        })
        .catch((error) => {
          console.error("MAPPA SECOES", error);
        });
    },
    getSecaoImg(secao) {
      let ramo =
        secao == "Alcatéia"
          ? "lobinho"
          : secao == "Tropa Escoteira"
          ? "escoteiro"
          : secao == "Tropa Sênior"
          ? "senior"
          : secao == "Clã Pioneiro"
          ? "pioneiro"
          : "escoteiro";
      ramo = "../../assets/logo_ramo_" + ramo + ".png"
      console.log("[AUTHMAPPA] getSecaoImg(" + secao + ")", ramo);
      return ramo
    },
  },
};
</script>

<style>
</style>