export const api_user_factory = function (axios) {
    const loadUserMenus = async function () {
        axios
            .get("/api/user/menu")
            .then(function (result) {
                this.menu_items = result;
            })
            .catch((error) => console.error("[USER MENU]", error));
    }

    const saveProfile = async function (profile) {
        try {
            let response = await axios.post("/api/user/profile", profile)
            return response.data
        } catch (error) {
            return error.response.data
        }
    }

    return { loadUserMenus, saveProfile }
}
