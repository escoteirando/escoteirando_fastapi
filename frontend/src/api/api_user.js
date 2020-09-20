import store from '../store'

export const api_user_factory = function (axios) {

    const isLogged = function () {
        return store.getters['backend/isLoggedUser']
    }
    /**
     * Get user menus from backend, caching into store
     */
    const getUserMenus = async function () {
        let menus = store.getters['user_menus/getNavMenu']
        if (menus == null || menus.length == 0) {
            try {
                const result = await axios.get("/api/user/menu")
                await store.dispatch('user_menus/setUserMenus', result.data)
                menus = result.data
                console.log('[API USER] MENUS', menus)
            } catch (error) {
                menus = null
                console.error('[API USER] MENUS', error)
            }
        } else {
            console.log('[API USER] MENUS (PREFETCHED)', menus)
        }
        return menus
    }

    const getUserCards = async function () {
        let cards = store.getters['user_menus/getCards']
        if (cards == null || cards.length == 0) {
            try {
                await store.dispatch("user_menus/load_user_cards")
                cards = store.getters['user_menus/getCards']
                console.log('[API USER] CARDS', cards)
            } catch (error) {
                cards = null
                console.error('[API USER] CARDS', error)
            }
        } else {
            console.log('[API USER CARDS (PREFETCHED)', cards)
        }
        return cards
    }


    const saveProfile = async function (profile) {
        try {
            let response = await axios.post("/api/user/profile", profile)
            return response.data
        } catch (error) {
            return error.response.data
        }
    }

    return { isLogged, getUserMenus, getUserCards, saveProfile }
}
