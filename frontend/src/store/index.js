import Vue from 'vue'
import Vuex from 'vuex'

import auth from './modules/auth'
import backend from './modules/backend'


Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        auth,
        backend
    }
})
