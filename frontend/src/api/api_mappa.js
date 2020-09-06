import store from '../store'

export const api_mappa_factory = function (axios) {
    // Efetua login no mappa atualizando o store e retornando informações do usuário
    const login = function (username, password) {
        return new Promise((resolve, reject) => {
            axios.post('/api/mappa/login', { username, password })
                .then(response => {
                    console.log('[API MAPPA] login', response.data)
                    store.dispatch('mappa/setMappa', response.data)
                    resolve(response.data)
                }).catch(error => {
                    console.error('[API MAPPA] login', error)
                    reject(error)
                })
        }
        )
    }

    // Consulta informações do usuário com autorização ainda válida
    const userInfo = function () {
        return new Promise((resolve, reject) => {
            axios.get('/api/mappa/user_info')
                .then(response => {
                    console.log('[API MAPPA] userInfo', response.data)
                    resolve(response.data)
                })
                .catch(error => {
                    console.error('[API MAPPA] userInfo', error)
                    reject(error)
                })
        })
    }

    // Retorna lista de seções do usuário
    const getSecoes = function () {
        return new Promise((resolve, reject) => {
            axios.get('/api/mappa/secoes')
                .then(response => {
                    console.log('[API MAPPA] getSecoes', response.data)
                    resolve(response.data)
                }).catch(error => {
                    console.error('[API MAPPA] getSecoes', error)
                    reject(error)
                })
        })
    }

    // Retorna lista de progressões do ramo
    const getProgressoes = function (codigo_ramo) {
        return new Promise((resolve, reject) => {
            axios.get('/api/mappa/lista_progressoes?codigo_ramo=' + codigo_ramo)
                .then(response => {
                    console.log('[API MAPPA] getProgressoes(' + codigo_ramo + ')', response.data)
                    resolve(response.data)
                }).catch(error => {
                    console.error('[API MAPPA] getProgressoes(' + codigo_ramo + ')', error)
                    reject(error)
                })
        })
    }



    return {
        login,
        userInfo,
        getSecoes,
        getProgressoes
    }
}
