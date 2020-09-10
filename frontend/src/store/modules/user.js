const EMPTY_STATE = {
    id: 0,
    nome_usuario: null,
    nome_completo: null,
    email: null,
    nascimento: null,
    sexo: null,
    nivel: null,
    nome_grupo: null,
    cod_grupo: null,
    cod_regiao: null,
    tipo_sessao: null,
    nome_sessao: null
}

const state = EMPTY_STATE

const getters = {
    getUser: (s) => s
}

const actions = {
    setUser({ commit }, user) {
        commit('SET_USER', user)
    }
}

const mutations = {
    SET_USER(s, user) {
        if (user.nascimento && user.nascimento.endsWith('+00:00')) {
            user.nascimento = user.nascimento.replace('+00:00', '-03:00')
        }
        s.nome_usuario = user.nome_usuario
        s.nome_completo = user.nome_completo
        s.email = user.email
        s.nascimento = new Date(user.nascimento)
        s.sexo = user.sexo
        s.nivel = user.nivel
        s.nome_grupo = user.nome_grupo
        s.cod_grupo = user.cod_grupo
        s.cod_regiao = user.cod_regiao
        s.tipo_sessao = user.tipo_sessao
        s.nome_sessao = user.nome_sessao
        console.log('[STORE USER]', { user: s })
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}