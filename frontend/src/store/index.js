import Vue from 'vue'
import Vuex from 'vuex'

import backend from './modules/backend'
import consts from './modules/consts'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        backend,
        consts
    }
})
