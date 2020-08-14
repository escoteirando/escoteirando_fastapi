import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueSeetalert2 from 'vue-sweetalert2'

import './plugins/api'

import vuetify from './plugins/vuetify';
import '@sweetalert2/theme-material-ui/material-ui.css'

Vue.use(VueSeetalert2)
Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App),
    vuetify,

    created() {
        // store.dispatch("auth/do_login", { username: "guionardo", password: "CogitoErgoSum@12$" })
        store.dispatch("auth/get_login_from_auth")
    }
}).$mount('#app')
