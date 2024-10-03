// store/modules/token.js

export default {
    state: {
        token: sessionStorage.getItem('token') || null,
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
            sessionStorage.setItem('token', token); 
        },
        clearToken(state) {
            state.token = null;
            sessionStorage.removeItem('token'); 
        }
    },
    getters: {
        token: (state) => state.token,
    }
};
