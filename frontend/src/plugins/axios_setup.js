import axios from "axios";

import { AuthHeader, AuthStorage, PropHeader, APIURL, APITimeout } from '@/api/consts'
import { local_storage_factory } from '@/api/local_storage'


let config = {
    baseURL: APIURL,
    timeout: APITimeout * 1000
};
const _axios = axios.create(config);
console.debug("API_SETUP", config)

_axios.interceptors.request.use(
    function(cfg) {
        if (!cfg.headers.common[AuthHeader]) {
            // console.log('[AXIOS] intercept config: ', config)
            let storage = local_storage_factory()
            let auth = storage.getValue(AuthStorage)
            let prop = storage.getValue(PropHeader)
            let log = []
            if (auth) {
                log.push({ auth: auth })
                cfg.headers.common[AuthHeader] = auth
                axios.defaults.headers.common[AuthHeader] = auth
            }
            if (prop) {
                log.push({ prop: prop })
                cfg.headers.common[PropHeader] = prop
                axios.defaults.headers.common[PropHeader] = prop
            }
            if (log.length > 0)
                console.log('[AXIOS] intercept', log)
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
