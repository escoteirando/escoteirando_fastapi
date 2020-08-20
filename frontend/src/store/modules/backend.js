import { AuthStorage } from '../../api/consts'
import { local_storage_factory } from '../../plugins/local_storage'

const local_storage = local_storage_factory()

const state = {
    host: "http://localhost:8000",
    auth: null,
    validUntil: 0,
    user: {
        name: null,
        email: null,
        ueb_id: 0,
        user_mappa: null
    }
}

const EMPTY_STATE = {
    host: "http://localhost:8000",
    auth: null,
    validUntil: 0,
    user: {
        name: null,
        email: null,
        ueb_id: 0,
        user_mappa: null
    }
}

const fetchPromise = (_fetch) => {
    let promise = new Promise((resolve, reject) => {
        _fetch
            .then(async response => {
                let json_response = response.json()
                if (response.ok) {
                    return resolve(json_response)
                }
                return reject(await json_response)
            })
            .catch(error => { reject(error) })
    })
    return promise
}

const getters = {
    getAuth: (s) => s.auth,
    getHost: (s) => s.host,
    getAuthorization: (s) => s.auth,
    isValid: (s) => s.validUntil > new Date().getTime() / 1000,
    getUser: (s) => s.user,
    get: (s) => (url, data = null) => {
        if (data) { url = url + "?" + new URLSearchParams(data).toString() }
        let _fetch = fetch(s.host + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': s.auth
            }
        })
        return fetchPromise(_fetch)
    },
    post: (s) => (url, data) => {
        let _fetch = fetch(s.host + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': s.auth
            },
            body: JSON.stringify(data)
        })
        return fetchPromise(_fetch)
    }
}

const actions = {
    setHost({ commit }, { host }) { commit('SET_HOST', host) },
    setAuth({ commit }, { auth }) { commit('SET_AUTH', auth) },
    getAuthFromStorage({ commit, dispatch }) {
        const authorization = local_storage.getValue(AuthStorage)
        if (!authorization) {
            console.log('[BACKEND] NO AUTHORIZATION DATA')
            return
        }
        console.log('[BACKEND] AUTHORIZATION FOUND', authorization)
        window.axios.post('/auth/user/' + authorization)
            .then(json => {
                commit('SET_LOGIN_DATA', json)
                dispatch('setAuth', { auth: json.authorization })
            })
            .catch(error => {
                local_storage.deleteValue(AuthStorage)
                commit('SET_LOGIN_DATA', EMPTY_STATE)
                console.error('[BACKEND] AUTH ERROR', error)
            })
    },
    set_login_data({ commit }, login_data) {
        commit('SET_LOGIN_DATA', login_data)
    },
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
        s.user_mappa = login_data.user_mappa
        local_storage.setValue(AuthStorage, login_data.authorization, login_data.validUntil)
        console.log('[BACKEND] SET LOGIN DATA', login_data)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
