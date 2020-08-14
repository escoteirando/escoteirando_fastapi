import axios from "axios";

import { AuthHeader, AuthStorage, APIURL, APITimeout } from '@/api/consts'
import { local_storage_factory } from './local_storage'


let config = {
    baseURL: APIURL,
    timeout: APITimeout * 1000
};
const _axios = axios.create(config);
console.debug("AXIOS_SETUP", config)
window.axios = _axios

_axios.interceptors.request.use(
    function(cfg) {
        if (!cfg.headers.common[AuthHeader]) {
            let storage = local_storage_factory()
            let auth = storage.getValue(AuthStorage)

            if (auth) {
                cfg.headers.common[AuthHeader] = auth
                axios.defaults.headers.common[AuthHeader] = auth
                console.log('[AXIOS] intercept', { auth })
            }

        }
        if (cfg.method.toLowerCase() == 'post') {
            console.log('[AXIOS] POST config', cfg)
        }
        return cfg;
    },
    function(error) {
        // Do something with request error
        return Promise.reject(error);
    }
);

// Add a response interceptor
_axios.interceptors.response.use(
    function(response) {
        // Do something with response data
        return response;
    },
    function(error) {
        // Do something with response error
        return Promise.reject(error);
    }
);

export {
    _axios
}
