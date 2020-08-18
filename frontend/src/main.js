import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import './plugins/api'

import VueSimpleAlert from "vue-simple-alert";
import vuetify from './plugins/vuetify';
import './assets/styles/swal.css'


Vue.use(VueSimpleAlert);

Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App),
    vuetify,

    created() {
        // store.dispatch("auth/do_login", { username: "guionardo", password: "CogitoErgoSum@12$" })
        store.dispatch("auth/get_login_from_auth")
        store.dispatch("consts/update_consts")
    }
}).$mount('#app')
