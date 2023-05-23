import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserView from '../views/UserView.vue'
import GoodSortView from '../views/GoodSortView.vue'
import ScoreView from '../views/ScoreView.vue'
import LoginView from '../views/LoginView.vue'
import IndexView from '../views/IndexView.vue'
import OrderView from '../views/OrderView.vue'
import DashboardView from "../views/DashboardView.vue"
import AboutView from "@/views/AboutView.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: IndexView
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView
        },
        {
            path: '/index',
            name: 'index',
            component: IndexView,
            children: [
                {
                    path: '/user',
                    component: UserView
                },
                {
                    path: '/score',
                    component: ScoreView
                },
                {
                    path: '/good-sort',
                    component: GoodSortView
                },
                {
                    path: '/order',
                    component: OrderView
                },
                {
                    path: "/exam",
                    component: () => import("../views/ExamView.vue")
                },
                {
                    path: "/goods",
                    component: () => import("../views/GoodView.vue")
                },
                {
                    path: "/dashboard",
                    component: DashboardView,
                    children: [
                        {
                            path: "/innerheader",
                            component: () => import("../components/InnerHeader.vue")
                        }
                    ]
                },
                {
                    path: "/account",
                    component: () => import("../views/AccountView.vue")
                }
            ]
        },
    ]
})

export default router
