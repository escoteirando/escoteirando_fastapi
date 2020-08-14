const currentLanguage = () => window.navigator.userLanguage || window.navigator.language || 'pt-br';

const msgPTBR = {
    'auth_login_ok': 'Login efetuado com sucesso',
    'auth_logout': 'Logout efetuado com sucesso',
    'auth_subscribe_ok': 'Registro do usuário efetuado com sucesso',
    'user_not_found': 'Usuário não encontrado',
    'user_not_created': 'Usuário não foi registrado',
    'user_not_created_saving': 'Erro ao gravar o usuário'
}

const msgs = {
    'ptbr': msgPTBR
}
export const getUserMessage = (code) => msgs[currentLanguage()][code] || `UNDEFINED MESSAGE ${code}`
