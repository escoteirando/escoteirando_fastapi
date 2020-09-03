import Vue from 'vue'
import VueRouter from 'vue-router'

import AuthLogin from '../views/auth/AuthLogin'
import AuthSubscribe from '../views/auth/AuthSubscribe'
import AuthPasswordResetRequest from '../views/auth/AuthPasswordResetRequest'
import AuthPasswordReset from '../views/auth/AuthPasswordReset'
import AuthMappa from '../views/auth/AuthMappa'
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


const testBackend = async (to) => {
    if (to.name == 'no_backend') {
        return true
    }
    try {
        let response = await window.axios.get('/api/hc', {}, { timeout: 500 })
        if (response.status == 200) {
            console.log('[BACKEND]', response.data)
            return true;
        }
        console.log('[BACKEND] TIMEOUT', response)
    } catch (error) {
        console.error("[BACKEND] OFFLINE", error)
    }
    return false;
}


const router = new VueRouter({ routes })
router.beforeEach(async (to, from, next) => {
    if (! await testBackend(to)) {
        next({
            name: 'no_backend',
            query: { redirect: to.fullPath }
        })
        return;
    }
    const isLoggedUser = await window.API.AUTH.verifyLoggedUser()
    console.log('[ROUTER] ' + (isLoggedUser ? 'LOGGED' : ''), to)

    if (isLoggedUser) {
        if (to.name !== 'login') {
            next()
            return
        }
        console.log('[ROUTER] LOGGED USER CANNOT LOGIN AGAIN')
        next({ name: 'home' })
        return
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
