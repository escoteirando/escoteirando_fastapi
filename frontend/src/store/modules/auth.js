const AUTH = 'ESCOTEIRANDO_AUTH'
const EMPTY_STATE = {
    authorization: null,
    validUntil: 0,
    user: {
        name: null,
        email: null
    }
}
const state = EMPTY_STATE

const getters = {
    getAuthorization: (s) => s.authorization,
    isValid: (s) => s.valid_until > new Date().getTime() / 1000,
    getUser: (s) => s.user
}

const actions = {
    do_login({ commit, rootGetters, dispatch }, { username, password }) {
        rootGetters['backend/post']('/auth/login', { username, password })
            .then(json => {
                commit('SET_LOGIN_DATA', json)
                dispatch("backend/setAuth", { auth: json.authorization }, { root: true })
            })
            .catch(error => {
                commit('SET_LOGIN_DATA', EMPTY_STATE)
                console.error('[AUTH] LOGIN ERROR', error)
            })
    },
    get_login_from_auth({ commit, rootGetters, dispatch }) {
        const authorization = window.localStorageEx.getValue(AUTH)
        if (!authorization) {
            console.log('[AUTH] NO AUTHORIZATION DATA')
            return
        }
        rootGetters['backend/post']('/auth/user/' + authorization)
            .then(json => {
                commit('SET_LOGIN_DATA', json)
                dispatch("backend/setAuth", { auth: json.authorization }, { root: true })
            })
            .catch(error => {
                commit('SET_LOGIN_DATA', EMPTY_STATE)
                console.error('[AUTH] AUTHORIZATION ERROR', error)
            })
    },
    get_login_from_auth_old({ commit, rootState }) {
        const authorization = window.localStorageEx.getValue(AUTH)
        if (!authorization) {
            console.log('[AUTH] NO AUTHORIZATION DATA')
            return
        }
        fetch(rootState.backend.host + "/auth/user/" + authorization, {
                method: "post"
            })
            // .then(response => response.json())
            .then(json => { commit('SET_LOGIN_DATA', json) })
            .catch(error => {
                console.error(error)
            })
    }

}


const mutations = {
    SET_LOGIN_DATA(s, login_data) {
        s.authorization = login_data.authorization
        s.validUntil = login_data.validUntil
        s.user = login_data.user
        window.localStorageEx.setValue('ESCOTEIRANDO_AUTH', login_data.authorization, login_data.validUntil)
        console.log('[AUTH] SET LOGIN DATA', login_data)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
