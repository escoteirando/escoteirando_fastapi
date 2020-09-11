export const AuthHeader = 'authorization'
export const APIURL = process.env.APIURL || 'http://localhost:8000'
export const APITimeout = 60
export const AuthStorage = 'ESCOTEIRANDO_AUTH'
export const MappaStorage = 'ESCOTEIRANDO_MAPPA'
export const ENVIRONMENT = process.env.PRODUCTION ? 'PRODUCTION' : 'DEVELOPMENT'

export const areas_desenvolvimento = [
    { id: "f", text: "Físico" },
    { id: "i", text: "Intelectual" },
    { id: "c", text: "Caráter" },
    { id: "a", text: "Afetivo" },
    { id: "s", text: "Social" },
    { id: "e", text: "Espiritual" },
]

export const tipos_atividade = [
    { id: 'c', text: 'Cerimônia' },
    { id: 'e', text: 'Instrução' },
    { id: 'h', text: 'História' },
    { id: 'i', text: 'Intervalo' },
    { id: 'j', text: 'Jogo' },
    { id: 'm', text: 'Canção' },
    { id: 'q', text: 'Quebra-gelo' }
]

export const tipos_atividade_educativos = ['e', 'h', 'j', 'm', 'q']

export const tipos_ramos = [
    { id: 'A', text: 'Alcatéia' },
    { id: 'E', text: 'Tropa Escoteira' },
    { id: 'S', text: 'Tropa Sênior' },
    { id: 'C', text: 'Clã Pioneiro' }
]


export const ramos = {
    1: { text: 'Alcatéia', logo: require('../assets/logo_ramo_lobinho.png') },
    2: { text: 'Tropa Escoteira', logo: require('../assets/logo_ramo_escoteiro.png') },
    3: { text: 'Tropa Sênior', logo: require('../assets/logo_ramo_senior.png') },
    4: { text: 'Clã Pioneiro', logo: require('../assets/logo_ramo_pioneiro.png') }
}

export const tipo_sexo = {
    'M': 'Masculino',
    'F': 'Feminino',
    'O': 'Outros'
}

export const tipo_membro_equipe = {
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