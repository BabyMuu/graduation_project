import {createStore} from 'vuex'

export default createStore({
    state: {
        Authorization: localStorage.getItem('Authorization') ? localStorage.getItem('Authorization') : '',
        username: localStorage.getItem('username') ? localStorage.getItem('username') : '',
        order: {}
    },
    getters: {
        getUsername(state) {
            return state.username
        }
    },
    mutations: {
        updateUsername(state, payload) {
            state.username = localStorage.getItem('username') ? localStorage.getItem('username') : ''
        },
    },
    actions: {},
    modules: {}
})
