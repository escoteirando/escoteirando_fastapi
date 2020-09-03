export const isValidEmail = (email) => (/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(email))

export const isValidUserName = (userName) => (/[a-zA-Z0-9.-]{5,20}/.test(userName))
export const userNameRules = "De 5 a 20 caracteres alfanuméricos, ponto e hífen"

import { ENVIRONMENT } from './consts'

const develop = ENVIRONMENT == 'DEVELOPMENT'

export const passwordRules = [
    (v) => v.length >= 5 || 'mínimo de 5 caracteres',
]

if (!develop) {
    passwordRules.push((v) => /[A-Z]/.test(v) || 'letras maiúsculas')
    passwordRules.push((v) => /[a-z]/.test(v) || 'letras minúsculas')
    passwordRules.push((v) => /\d/.test(v) || "números")
    passwordRules.push((v) => /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(v) || 'símbolos')
}

export const passwordNeeds = (password) => {
    let msgRequer = [];
    if (!develop) {
        if (!/\d/.test(password)) {
            msgRequer.push("número(s)")
        }
        if (!/[A-Z]/.test(password)) {
            msgRequer.push("letra(s) maiúscula(s)")
        }
        if (!/[a-z]/.test(password)) {
            msgRequer.push("letra(s) minúscula(s)")
        }
        if (!/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password)) {
            msgRequer.push("símbolo(s)")
        }
    }
    if (password.length < 5) {
        msgRequer.push("mínimo de 5 caracteres")
    }
    return msgRequer
}

export const isValidPassword = (password) => passwordNeeds(password).length == 0

export const dateAsString = (date) =>
    date ? date.toLocaleDateString() : "00/00/0000"

export const checkOnlineStatus = async () => {
    const hosts = ['https://google.com',
        'https://yahoo.com',
        'https://msn.com']

    try {
        let p = await Promise.race(hosts.map(x => fetch(x, { method: 'HEAD' })))
        console.log("ONLINE", p)
        return true
    } catch (error) {
        console.error("[ONLINE] ERROR", error)
    }
    return false
}