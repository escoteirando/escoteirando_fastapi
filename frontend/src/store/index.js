import Vue from 'vue'
import Vuex from 'vuex'

import backend from './modules/backend'
import consts from './modules/consts'
import mappa from './modules/mappa'
import user_menus from './modules/user_menus'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        backend,
        consts,
        mappa,
        user_menus,
        user
    }
})
