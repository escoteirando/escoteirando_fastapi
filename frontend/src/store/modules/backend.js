const state = {
    host: "http://localhost:8000",
    auth: null
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
    getHost: (s) => s.host,
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
    setAuth({ commit }, { auth }) { commit('SET_AUTH', auth) }
}

const mutations = {
    SET_HOST(s, host) { s.host = host },
    SET_AUTH(s, auth) { s.auth = auth }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
