import { local_storage_factory, currentTimeStamp } from '../../plugins/local_storage'

const local_storage = local_storage_factory()

const state = {
    tipo_atv: {},
    area_desenv: {}
}


const getters = {
    get_tipo_atv: (s) => s.tipo_atv,
    get_area_desenv: (s) => s.area_desenv
}

const actions = {
    update_consts({ commit, rootGetters }) {
        let consts = local_storage.getValue('_consts', null)
        if (consts) {
            console.log('[CONSTS] FROM LOCAL STORAGE', consts)
            commit('UPDATE_CONSTS', consts)
        } else {
            rootGetters['backend/get']('/api/consts')
                .then(function (consts) {
                    console.log('[CONSTS]', consts)
                    local_storage.setValue('_consts', consts, currentTimeStamp() + 60 * 60)
                    commit('UPDATE_CONSTS', consts)
                })
                .catch(error => console.error('[CONSTS]', error))
        }
    }
}

const mutations = {
    UPDATE_CONSTS(s, consts) {
        s.area_desenv = consts.area_desenv
        s.tipo_atv = consts.tipo_atv
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}