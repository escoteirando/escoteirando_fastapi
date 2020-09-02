import store from '../store'
import { AuthStorage } from './consts'
import { local_storage_factory } from '../plugins/local_storage'

const storage = local_storage_factory()

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

    const verifyLoggedUser = async function () {
        await store.dispatch("backend/getAuthFromStorage")
        const isLoggedUser = storage.getValue(AuthStorage, false)
        console.debug('[AUTH] verifyLoggedUser', isLoggedUser)
        return isLoggedUser
    }

    const getLoggedUser = async function () {
        const auth = storage.getValue(AuthStorage, false)
        if (!auth) return null
        let user = store.getters['backend/getUser']
        if (!user) {
            await store.dispatch("backend/getAuthFromStorage")
            user = store.getters['backend/getUser']
        }
        return user
    }

    return {
        login,
        subscribe,
        verifyLoggedUser,
        getLoggedUser
    }
}
