const state = {
    authorization = null,
    validUntil = 0
}

const getters = {
    getAuthorization: (s) => s.authorization,
    isValid: (s) => s.valid_until > new Date().getTime() / 1000
}

const actions = {
    do_login({ commit }, { username, password }) {
        fetch({ method: "post", url: "/auth/login", data: { username: username, password: password })
            .then(response => {

            })
            .catch(error => {

            })
    },
    do_read_fr
}

const mutations = {

}