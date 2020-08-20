import Vue from 'vue'
import VueRouter from 'vue-router'
import AuthLogin from '../views/auth/AuthLogin'
import AuthSubscribe from '../views/auth/AuthSubscribe'
import AuthPasswordResetRequest from '../views/auth/AuthPasswordResetRequest'
import AuthPasswordReset from '../views/auth/AuthPasswordReset'

import Testing from '../views/Testing'

import Home from '../views/Home'
import store from '../store'

Vue.use(VueRouter)

const routes = [
    { path: '/', name: 'home', meta: { title: "Escoteirando" }, component: Home },
    { path: '/auth/login', name: 'login', meta: { title: "Escoteirando : Login" }, component: AuthLogin },
    { path: '/auth/subscribe', name: 'subscribe', meta: { title: "Escoteirando : Registrar" }, component: AuthSubscribe },
    { path: '/auth/reset', name: 'reset', component: AuthPasswordResetRequest },
    { path: '/auth/redefine', name: 'redefine', component: AuthPasswordReset },
    { path: '/test', name: 'test', component: Testing }
]

const freeRoutes = ['login', 'subscribe', 'reset', 'redefine', 'test']

const router = new VueRouter({ routes })
router.beforeEach((to, from, next) => {
    const isAuthorized = store.getters["backend/isValid"]
    if ((freeRoutes.indexOf(to.name) >= 0) || isAuthorized) {
        next()
    } else {
        next()
        // console.log(`Routing to ${to.name} but not authorized: Redirecting to login`)
        // next({
        //     path: '/auth/login',
        //     query: { redirect: to.fullPath }
        // })
    }
})
export default router
