import store from '../store'

export const api_auth_factory = function (axios) {

    const login = function (username, password) {
        return new Promise((resolve, reject) => {
            axios.post('/auth/login', { username, password })
                .then(response => {
                    store.dispatch('backend/set_login_data', response.data)
                    resolve(response)
                }).catch(error => {
                    reject(error)
                })
        })
    }

    const subscribe = function (username, email, password) {
        return axios.post('/auth/subscribe', { username, password, email, ueb_id: 0 });
    }

    return {
        login,
        subscribe
    }
}
