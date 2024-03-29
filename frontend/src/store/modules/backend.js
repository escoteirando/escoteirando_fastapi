import { AuthStorage, APIURL } from '../../api/consts'
import { local_storage_factory, currentTimeStamp } from '../../plugins/local_storage'
import router from '../../router'

const local_storage = local_storage_factory()

const EMPTY_STATE = {
    host: APIURL,
    auth: null,
    validUntil: 0,
    user: {
        id: 0,
        name: null,
        full_name: null,
        email: null,
        ueb_id: 0,
        user_mappa: null
    },
    healthy: false
}

const state = EMPTY_STATE

const getters = {
    getAuth: (s) => s.auth,
    getHost: (s) => s.host,
    getAuthorization: (s) => s.auth,
    isLoggedUser: (s) => (s.auth && s.auth.authorization && s.auth.authorization.length > 0 && s.validUntil > currentTimeStamp),
    getUser: (s) => s.user,
    isHealthy: (s) => s.healthy
}

const actions = {
    setHost({ commit }, { host }) { commit('SET_HOST', host) },
    setAuth({ commit, dispatch }, { auth }) {
        const user = {
            id: auth.user.id,
            nome_usuario: auth.user.name,
            nome_completo: auth.user.full_name,
            email: auth.email,
            nascimento: auth.user.nascimento,
            sexo: auth.user.sexo,
            nivel: null,
            nome_grupo: null,
            cod_grupo: null,
            cod_regiao: null,
            tipo_sessao: null,
            nome_sessao: null
        }
        dispatch('user/setUser', user, { root: true })
        commit('SET_AUTH', auth)
    },
    getAuthFromStorage({ commit, dispatch }) {
        const authorization = local_storage.getValue(AuthStorage)
        if (!authorization) {
            commit('SET_LOGIN_DATA', EMPTY_STATE)
            local_storage.deleteValue(AuthStorage)
            console.log('[BACKEND] NO AUTHORIZATION DATA')
            return
        }
        console.log('[BACKEND] AUTHORIZATION FOUND', authorization)
        window.axios.post('/auth/user/' + authorization)
            .then(json => {
                json = json.data
                console.log('[BACKEND] DATA FROM AUTH', json)
                commit('SET_LOGIN_DATA', json)
                dispatch('setAuth', { auth: json })
                dispatch('user_menus/load_user_menus', {}, { root: true })
            })
            .catch(error => {
                local_storage.deleteValue(AuthStorage)
                commit('SET_LOGIN_DATA', EMPTY_STATE)
                console.error('[BACKEND] AUTH ERROR', error)
            })
    },
    setLoginData({ commit }, login_data) {
        commit('SET_LOGIN_DATA', login_data)
    },
    clearLogin({ commit }) {
        console.log('[BACKEND] CLEAR LOGIN')
        commit('SET_LOGIN_DATA', EMPTY_STATE)
    },
    logout({ commit }) {
        commit('SET_LOGOUT')
        router.push({ name: 'login' })
        router.go()
    },
    checkBackend({ commit }) {
        window.axios.get('/api/hc')
            .then(() => {
                commit('SET_HEALTHY', true)
            }).catch((error) => {
                console.error('BACKEND NOT HEALTHY', error)
                commit('SET_HEALTHY', false)
            })
    }

}

const mutations = {
    SET_HOST(s, host) { s.host = host },
    SET_AUTH(s, auth) { s.auth = auth },
    SET_LOGIN_DATA(s, login_data) {
        s.auth = login_data.authorization
        s.validUntil = login_data.validUntil
        s.user = login_data.user
        s.validUntil = login_data.validUntil
        s.ueb_id = login_data.ueb_id
        local_storage.setValue(AuthStorage, login_data.authorization, login_data.validUntil)
        console.log('[BACKEND] SET LOGIN DATA', login_data)
    },
    SET_LOGOUT(s) {
        console.log('[BACKEND] LOGOUT')
        local_storage.deleteValue(AuthStorage)
        s.auth = null
        s.validUntil = 0
        s.user = {
            name: null,
            email: null,
            ueb_id: 0,
            mappa_user: null
        }
    },
    SET_HEALTHY(s, healthy) {
        s.healthy = healthy
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
