import router from '@/router'

const state = {
    nav_menu: [{ id: 999, text: "Sair", icon: "mdi-exit-to-app", action: "logout" }],
    cards: []
}
const getters = {
    getNavMenu: s => s.nav_menu,
    getCards: s => s.cards
}

const actions = {
    load_user_menus({ commit }) {
        window.axios
            .get("/api/user/menu")
            .then(function (result) {
                commit('SET_USER_MENUS', result.data)
            })
            .catch((error) => console.error("[USER MENU]", error));
    },
    load_user_cards({ commit }) {
        window.axios
            .get("/api/user/home")
            .then((result) => {
                commit('SET_USER_CARDS', result.data)
            })
            .catch((error) => console.error("[HOME] CARDS", error));
    },
    setUserMenus({ commit }, menus) {
        commit('SET_USER_MENUS', menus)
    },
    setUserCards({ commit }, cards) {
        commit('SET_USER_CARDS', cards)
    },
    callAction({ dispatch }, action_id) {
        let actionLog = ''
        switch (action_id) {
            case 1:
                actionLog = 'USER PROFILE'
                router.push({ name: '' })
                break
            case 888:
                actionLog = 'mAPPa credentials'
                router.push({ name: 'mappa' })
                break;
            case 999:
                actionLog = 'LOGOUT'
                dispatch("backend/logout", {}, { root: true })
                break;
            default:
                console.warn('[USER MENU] INVALID ACTION ID', action_id)
                return
        }
        console.log('[USER MENU] ACTION', actionLog)
    }
}
const mutations = {
    SET_USER_MENUS(s, menus) {
        console.log('[MENUS]', menus)
        s.nav_menu = menus
    },
    SET_USER_CARDS(s, cards) {
        console.log('[CARDS]', cards)
        s.cards = cards
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}