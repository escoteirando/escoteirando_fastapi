"use strict";

import Vue from 'vue'

import { _axios } from './axios_setup'
import { local_storage_factory } from './local_storage'
import { api_auth_factory } from '../api/api_auth'
import { api_mappa_factory } from '../api/api_mappa'
import { api_user_factory } from '../api/api_user'
let _api = {}
try {

    const LOCAL_STORAGE = local_storage_factory()
    const AUTH = api_auth_factory(_axios, LOCAL_STORAGE)
    const MAPPA = api_mappa_factory(_axios)
    const USER = api_user_factory(_axios)

    _api = {
        LOCAL_STORAGE: LOCAL_STORAGE,
        AUTH: AUTH,
        MAPPA: MAPPA,
        USER: USER
    }
} catch (err) {
    console.error('ERRO EM API.js', err)
    throw "Deu pau"
}


Plugin.install = function (vue) {
    // vue.axios = _axios;
    vue.API = _api
    window.API = _api

    Object.defineProperties(vue.prototype, {
        // axios: {get() { return _axios; } },
        // $axios: {get() { return _axios; } },
        API: { get() { return _api } },
        $API: { get() { return _api } }
    });
    console.log('[API] INIT', _api)
};

Vue.use(Plugin)

export default Plugin;
