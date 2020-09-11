import store from '../store'
import { AsyncLock } from './async_lock'


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
    const lockGUI = new AsyncLock()

    const getUserInfo = async function () {
        await lockGUI.promise
        lockGUI.enable()
        const mappa_user = store.getters['backend/getUser'].mappa_user
        let user_info = null
        if (mappa_user) {
            user_info = store.getters['mappa/getMappa']
            if (user_info.user_id == 0) {
                try {
                    user_info = await window.API.MAPPA.userInfo()
                    if (user_info.user_id) {
                        store.dispatch('mappa/setMappa', user_info)
                    }
                } catch (error) {
                    console.error('[API MAPPA] USER_INFO', error)
                    user_info = null
                }
            }
        }
        lockGUI.disable()
        return user_info
    }

    const lockGS = new AsyncLock()

    const getSecao = async function () {
        await lockGS.promise
        lockGS.enable()
        let secoes = store.getters['backend/getSecoes']
        let secao = null
        if (secoes && secoes.length > 0) {
            secao = secoes[0]
            console.log('[API MAPPA] SECAO', secao)
        } else {
            try {
                secoes = await window.API.MAPPA.getSecoes()
                if (secoes && secoes.length > 0) {
                    secao = secoes[0]
                    store.dispatch('mappa/setSecoes', secoes)
                    console.log('[API MAPPA] SECAO (FROM BACKEND)', secao)
                }
            } catch (error) {
                console.error('[API MAPPA] SECOES', error)
                secao = null
            }
        }
        lockGS.disable()
        return secao
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

    const lockGE = new AsyncLock()

    const getEquipe = async function (codigo_secao) {
        await lockGE.promise
        lockGE.enable()
        let equipes = store.getters['backend/getEquipe']
        if (equipes && equipes.length > 0) {
            console.log('[API MAPPA] EQUIPE', equipes)
        } else {
            try {
                equipes = await window.API.MAPPA.fetchEquipe(codigo_secao)
                if (equipes && equipes.length > 0) {
                    store.dispatch('mappa/setEquipe', equipes)
                    console.log('[API MAPPA] EQUIPE (FROM BACKEND)', equipes)
                } else {
                    equipes = null
                }
            } catch (error) {
                console.error('[API MAPPA] EQUIPE', error)
                equipes = null
            }
        }
        lockGE.disable()
        return equipes
    }
    const fetchEquipe = function (codigo_secao) {
        return new Promise((resolve, reject) => {
            axios.get(`/api/mappa/equipe/${codigo_secao}`)
                .then(response => {
                    console.log('[API MAPPA getEquipe(' + codigo_secao + ')', response.data)
                    resolve(response.data)
                }).catch(error => {
                    console.log('[API MAPPA getEquipe(' + codigo_secao + ')', error)
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
        getUserInfo,
        getSecao,
        getSecoes,
        getProgressoes,
        getEquipe,
        fetchEquipe
    }
}
