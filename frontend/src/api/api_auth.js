import store from '../store'
import { AuthStorage } from './consts'


export const api_auth_factory = function (axios, storage) {

    const login = function (username, password) {
        return new Promise((resolve, reject) => {
            axios.post('/auth/login', { username, password })
                .then(response => {
                    store.dispatch('backend/setLoginData', response.data)
                    resolve(response)
                }).catch(error => {
                    reject(error)
                })
        })
    }

    const subscribe = function (username, email, password) {
        return axios.post('/auth/subscribe', { username, password, email });
    }

    const verifyLoggedUser = async function (forceFetch = false) {
        const auth = storage.getValue(AuthStorage, false)
        if (!auth) {
            console.log('[API AUTH] verifyLoggedUser', 'NO AUTHORIZATION')
            return false
        }
        let user = store.getters['backend/getUser']
        if (!user.id || forceFetch) {
            console.log('[API AUTH] AUTHORIZATION FOUND', auth)
            try {
                let json = await axios.post('/auth/user/' + auth)
                console.log('[API AUTH] verifyLoggedUser post', json)
                store.dispatch('backend/setLoginData', json.data)
            } catch (error) {
                storage.deleteValue(AuthStorage)
                store.dispatch('backend/clearLogin')
                console.error('[API AUTH] AUTH ERROR', error)
                return false
            }
        }
        return true

        // await store.dispatch("backend/getAuthFromStorage")
        // const isLoggedUser = storage.getValue(AuthStorage, false)
        // console.debug('[AUTH] verifyLoggedUser', isLoggedUser)
        // return isLoggedUser
    }

    const getLoggedUser = async function () {
        let user = store.getters['backend/getUser']

        return user
    }

    return {
        login,
        subscribe,
        verifyLoggedUser,
        getLoggedUser,
    }
}
