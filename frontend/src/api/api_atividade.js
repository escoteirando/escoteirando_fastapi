export const api_atividade_factory = function (axios) {
    const salvarAtividade = async function (atividade) {
        try {
            let response = await axios.post("/api/atividade", atividade)
            return response.data
        } catch (error) {
            return error.response.data
        }
    }

    return { salvarAtividade }
}

