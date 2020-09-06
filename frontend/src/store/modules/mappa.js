import { MappaStorage } from '../../api/consts'
import { local_storage_factory } from '../../plugins/local_storage'

const local_storage = local_storage_factory()
const storage_login = MappaStorage + '_LOGIN'
const storage_secoes = MappaStorage + '_SECOES'

const state = {
    mappa: {
        auth_valid_until: 0,
        authorization: null,
        cod_grupo: 0,
        cod_modalidade: null,
        cod_regiao: null,
        nom_grupo: null,
        nome_completo: null,
        user_id: 0,
        sexo: null,
        nascimento: null,
        email: null
    },
    secoes: []
}
const getters = {
    getMappa: (s) => s.mappa,
    getSecoes: (s) => s.secoes
}

const actions = {
    getMappaFromStorage({ commit }) {
        const mappa = local_storage.getValue(storage_login)
        const secoes = local_storage.getValue(storage_secoes)
        console.log('[MAPPA] DATA', { mappa, secoes })
        if (mappa) {
            commit('SET_MAPPA', mappa)
        }
        if (secoes) {
            commit('SET_SECOES', secoes)
        }
    },
    setMappa({ commit }, mappa) {
        commit('SET_MAPPA', mappa)
        local_storage.setValue(storage_login, mappa, mappa.auth_valid_until)
    },
    setSecoes({ commit }, secoes) {
        commit('SET_SECOES', secoes)
        local_storage.setValue(storage_secoes, secoes)
    }
}
const mutations = {
    SET_MAPPA(s, mappa) {
        // Tratar data de nascimento
        // 1977-02-05T00:00:00+00:00
        if (mappa.nascimento.endsWith('+00:00')) {
            mappa.nascimento = mappa.nascimento.replace('+00:00', '-03:00')
        }
        s.mappa = {
            auth_valid_until: mappa.auth_valid_until,
            authorization: mappa.authorization,
            cod_grupo: mappa.cod_grupo,
            cod_modalidade: mappa.cod_modalidade,
            cod_regiao: mappa.cod_regiao,
            nom_grupo: mappa.nom_grupo,
            nome_completo: mappa.nome_completo,
            user_id: mappa.user_id,
            sexo: mappa.sexo,
            nascimento: new Date(mappa.nascimento),
            email: mappa.email
        }
    },
    SET_SECOES(s, secoes) {
        s.secoes = secoes
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
