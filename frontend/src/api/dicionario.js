const dicionario = {
    ramo: {
        1: { id: 'A', text: 'Lobinho', logo: require('../assets/logo_ramo_lobinho.png') },
        2: { id: 'E', text: 'Escoteiro', logo: require('../assets/logo_ramo_escoteiro.png') },
        3: { id: 'S', text: 'Sênior', logo: require('../assets/logo_ramo_senior.png') },
        4: { id: 'C', text: 'Pioneiro', logo: require('../assets/logo_ramo_pioneiro.png') }
    },
    area: {
        1: { id: "f", text: "Físico" },
        2: { id: "i", text: "Intelectual" },
        3: { id: "c", text: "Caráter" },
        4: { id: "a", text: "Afetivo" },
        5: { id: "s", text: "Social" },
        6: { id: "e", text: "Espiritual" },
    },
    atividade: {
        1: { id: 'c', text: 'Cerimônia', educ: false },
        2: { id: 'e', text: 'Instrução', educ: true },
        3: { id: 'h', text: 'História', educ: true },
        4: { id: 'i', text: 'Intervalo', educ: false },
        5: { id: 'j', text: 'Jogo', educ: true },
        6: { id: 'm', text: 'Canção', educ: true },
        7: { id: 'q', text: 'Quebra-gelo', educ: true },
        8: { id: 'o', text: 'Comunidade', educ: true }
    },
    sexo: {
        1: { id: 'M', text: 'Masculino' },
        2: { id: 'F', text: 'Feminino' },
        3: { id: 'O', text: 'Outros' },
    },
    membro_equipe: {
        1: { 1: { 'M': "Primo", 'F': "Prima" }, 2: { 'M': "Segundo", 'F': 'Segunda' }, 0: { 'M': "Lobo", 'F': 'Loba' } },
        2: {
            1: { 'M': "Monitor", 'F': 'Monitora' }, 2: { 'M': "Submonitor", 'F': 'Submonitora', 0: { 'M': "Patrulheiro", 'F': 'Patrulheira' } }
        },
        3: {
            1: { 'M': "Monitor", 'F': 'Monitora' }, 2: { 'M': "Submonitor", 'F': 'Submonitora', 0: { 'M': "Patrulheiro", 'F': 'Patrulheira' } }
        },
        4: {
            1: { 'M': "Monitor", 'F': 'Monitora' }, 2: { 'M': "Submonitor", 'F': 'Submonitora', 0: { 'M': "Patrulheiro", 'F': 'Patrulheira' } },
        }
    }

}

export const getDict = (dominio, id) => {
    try {
        if (dominio in dicionario) {
            if (typeof (id) == "number") {
                if (id in dicionario[dominio]) {
                    return dicionario[dominio][id]
                }
            }
            let result = null
            Object.keys(dicionario[dominio]).forEach(element => {
                if (dicionario[dominio][element].id == id)
                    result = dicionario[dominio][element]
            });
            return result
        } else {
            throw Error(`DOMAIN INEXISTENT ${dominio}`)
        }
    } catch (error) {
        console.error('ERROR GETTING DICTIONARY', { dominio, id, error })
    }
    return null
}

export const getDictAsList = (dominio) => {
    if (dominio in dicionario) {
        return Object.values(dicionario[dominio])
    }
    console.error()
    return null

}