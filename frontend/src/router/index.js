import Vue from 'vue'
import VueRouter from 'vue-router'
import AuthLogin from '../views/auth/AuthLogin'
import AuthSubscribe from '../views/auth/AuthSubscribe'
import AuthPasswordResetRequest from '../views/auth/AuthPasswordResetRequest'
import AuthPasswordReset from '../views/auth/AuthPasswordReset'
import { local_storage_factory } from '../plugins/local_storage'
import { AuthStorage } from '../api/consts'
import Testing from '../views/Testing'
import Error404 from '../views/Error404'

import Home from '../views/Home'

Vue.use(VueRouter)

const routes = [
    { path: '/', name: 'home', meta: { title: "Escoteirando" }, component: Home },
    { path: '/auth/login', name: 'login', meta: { title: "Escoteirando : Login" }, component: AuthLogin },
    { path: '/auth/subscribe', name: 'subscribe', meta: { title: "Escoteirando : Registrar" }, component: AuthSubscribe },
    { path: '/auth/reset', name: 'reset', component: AuthPasswordResetRequest },
    { path: '/auth/redefine', name: 'redefine', component: AuthPasswordReset },
    { path: '/test', name: 'test', component: Testing },
    { path: '*', name: '404', component: Error404 }
]

const freeRoutes = ['login', 'subscribe', 'reset', 'redefine', 'test','404']
const storage = local_storage_factory()

const router = new VueRouter({ routes })
router.beforeEach((to, from, next) => {
    const isLoggedUser = storage.getValue(AuthStorage, false)

    if (isLoggedUser) {
        if (to.name == 'login') {
            console.log('[ROUTER] LOGGED USER CANNOT LOGIN AGAIN')
            next({ path: '/' })
        } else {
            next()
        }
    }
    else if (freeRoutes.indexOf(to.name) < 0) {
        console.log(`[ROUTER] Routing to ${to.name} but not authorized: Redirecting to login`)
        next({
            path: '/auth/login',
            query: { redirect: to.fullPath }
        })
    } else {
        next()
    }

})
export default router
