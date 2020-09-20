import { MappaStorage } from '../../api/consts'
import { local_storage_factory } from '../../plugins/local_storage'

const local_storage = local_storage_factory()
const storage_login = MappaStorage + '_LOGIN'
const storage_secoes = MappaStorage + '_SECOES'
const storage_equipe = MappaStorage + '_EQUIPE'
const storage_progressoes = MappaStorage + '_PROGRESSOES'

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
        mappa_user: null
    },
    secoes: [],
    equipe: [
        {
            codigo: 0,
            nome: null,
            codigoSecao: 0,
            codigoLider: 0,
            codigoViceLider: 0,
            associados: [
                {
                    codigo: 0,
                    nome: null,
                    dataNascimento: "2020-09-11T01:10:45.318Z",
                    sexo: null
                }]
        }
    ],
    progressoes: {
        'A': [],
        'E': [],
        'S': [],
        'P': []
    }
}
const getters = {
    getMappa: (s) => s.mappa,
    getSecoes: (s) => s.secoes,
    getEquipe: (s) => s.equipe,
    getProgressoes: (s) => s.progressoes
}

const actions = {
    getMappaFromStorage({ commit }) {
        const mappa = local_storage.getValue(storage_login)
        const secoes = local_storage.getValue(storage_secoes)
        const progressoes = {}
        const ramos = ['A', 'E', 'S', 'P']
        ramos.forEach(function (x) {
            progressoes[x] = local_storage.getValue(storage_progressoes + '_' + x)
        })
        console.log('[MAPPA] DATA', { mappa, secoes, progressoes })
        if (mappa) {
            commit('SET_MAPPA', mappa)
        }
        if (secoes) {
            commit('SET_SECOES', secoes)
        }
        ramos.forEach(function (x) {
            if (progressoes[x]) {
                commit('SET_PROGRESSOES', x, progressoes[x])
            }
        })
    },
    setMappa({ commit }, mappa) {
        commit('SET_MAPPA', mappa)
        local_storage.setValue(storage_login, mappa, mappa.auth_valid_until)
    },
    setSecoes({ commit }, secoes) {
        commit('SET_SECOES', secoes)
        local_storage.setValue(storage_secoes, secoes)
    },
    setEquipe({ commit }, equipe) {
        commit('SET_EQUIPE', equipe)
        local_storage.setValue(storage_equipe, equipe)
    },
    setProgressoes({ commit }, { ramo, progressoes }) {
        commit('SET_PROGRESSOES', { ramo, progressoes })
        local_storage.setValue(storage_progressoes + '_' + ramo, progressoes)
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
            mappa_user: mappa.mappa_user
        }
    },
    SET_SECOES(s, secoes) {
        s.secoes = secoes
    },
    SET_EQUIPE(s, equipe) {
        s.equipe = equipe
    },
    SET_PROGRESSOES(s, { ramo, progressoes }) {
        s.progressoes[ramo] = progressoes
        console.log('[STORE MAPPA] PROGRESSOES ' + ramo, progressoes)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
