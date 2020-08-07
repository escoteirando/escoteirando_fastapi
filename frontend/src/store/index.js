import Vue from 'vue'
import Vuex from 'vuex'

import auth from './modules/auth'
import backend from './modules/backend'
import { setup_local_storage } from './modules/local_storage'


setup_local_storage()

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        auth,
        backend
    }
})
