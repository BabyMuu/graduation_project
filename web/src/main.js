import {createApp} from 'vue'
import {createPinia} from 'pinia'

import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/assets/init.css'
import axios from "axios";
import VueAxios from 'vue-axios'
import store from "./stores";
import moment from 'moment'

import echarts from "@/assets/echarts"

axios.defaults.baseURL = 'http://127.0.0.1:8088/'

axios.defaults.xsrfCookieName = 'csrfmiddlewaretoken'
axios.defaults.xsrfHeaderName = 'X-XSRF-TOKEN'
//重点！！！设置请求获取cookie
axios.defaults.withCredentials = true
// 添加请求拦截器，在请求头中加token
// axios.interceptors.request.use(
//     config => {
//         if (localStorage.getItem('username')) {
//             config.headers.Username = localStorage.getItem('username');
//         }
//         return config;
//     },
//     error => {
//         return Promise.reject(error);
//     });

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(VueAxios, axios)
app.use(store)
app.config.globalProperties.$moment = moment
app.config.globalProperties.$echarts = echarts
app.mount('#app')
