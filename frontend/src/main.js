import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import { setup_local_storage } from '@/store/modules/local_storage'

setup_local_storage()
Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App),
    created() {
        // store.dispatch("auth/do_login", { username: "guionardo", password: "CogitoErgoSum@12$" })
        store.dispatch("auth/get_login_from_auth")
    }
}).$mount('#app')
