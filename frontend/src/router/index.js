import Vue from 'vue'
import VueRouter from 'vue-router'

import AuthLogin from '../views/auth/AuthLogin'
import AuthSubscribe from '../views/auth/AuthSubscribe'
import AuthPasswordResetRequest from '../views/auth/AuthPasswordResetRequest'
import AuthPasswordReset from '../views/auth/AuthPasswordReset'
import AuthMappa from '../views/auth/AuthMappa'
import { local_storage_factory } from '../plugins/local_storage'
import { AuthStorage } from '../api/consts'
import Testing from '../views/Testing'
import Error404 from '../views/errors/Error404'
import ErrorBackend from '../views/errors/ErrorBackend'
import UserProfile from '../views/user/UserProfile'

// import store from '../store'

import Home from '../views/Home'

Vue.use(VueRouter)

const routes = [
    { path: '/', name: 'home', meta: { title: "Escoteirando" }, component: Home },
    { path: '/auth/login', name: 'login', meta: { title: "Escoteirando : Login" }, component: AuthLogin },
    { path: '/auth/subscribe', name: 'subscribe', meta: { title: "Escoteirando : Registrar" }, component: AuthSubscribe },
    { path: '/auth/reset', name: 'reset', component: AuthPasswordResetRequest },
    { path: '/auth/redefine', name: 'redefine', component: AuthPasswordReset },
    { path: '/auth/mappa', name: 'mappa', component: AuthMappa },
    { path: '/user/profile', name: 'profile', component: UserProfile },
    { path: '/test', name: 'test', component: Testing },
    { path: '/no_backend', name: 'no_backend', component: ErrorBackend },
    { path: '*', name: '404', component: Error404 }
]

const freeRoutes = ['login', 'subscribe', 'reset', 'redefine', 'test', '404', 'no_backend']
const storage = local_storage_factory()

const testBackend = async () => {
    try {
        let response = await window.axios.get('/api/hc')
        if (response.status == 200) {
            console.log('[BACKEND]', response.data)
            return true;
        }
    } catch (error) {
        console.error("[BACKEND] OFFLINE", error)
    }
    return false;
}

const router = new VueRouter({ routes })
router.beforeEach((to, from, next) => {
    if (to.name != 'no_backend' && !testBackend()) {
        next({
            name: 'no_backend',
            query: { redirect: to.fullPath }
        })
        return;
    }
    const isLoggedUser = storage.getValue(AuthStorage, false)
    console.log('[ROUTER] ' + (isLoggedUser ? 'LOGGED' : ''), to)
    if (isLoggedUser) {
        if (to.name == 'login') {
            console.log('[ROUTER] LOGGED USER CANNOT LOGIN AGAIN')
            next({ name: 'home' })
            return
        } else if (to.name != 'mappa') {
            // const user = store.getters['backend/getUser']
            // console.log('[ROUTER] user', user)
            // if (user.ueb_id == 0 && !user.mappa_user) {
            //     console.log('[ROUTER] ASKING FOR MAPPA USER')
            //     next({
            //         name: 'mappa',
            //         query: { redirect: to.fullPath }
            //     })
            //     return
            // }
        }
        next()

    }
    else if (freeRoutes.indexOf(to.name) < 0) {
        console.log(`[ROUTER] Routing to ${to.name} but not authorized: Redirecting to login`)
        next({
            name: 'login',
            query: { redirect: to.fullPath }
        })
    } else {
        next()
    }

})


export default router
