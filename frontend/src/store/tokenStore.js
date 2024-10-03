import { defineStore } from 'pinia';

export const useTokenStore = defineStore('tokenStore', {
  state: () => ({
    token: null,
  }),
  actions: {
    setToken(token) {
      this.token = token;
    },
    clearToken() {
      this.token = null;
    },
  },
  getters: {
    getToken: (state) => state.token,
  },
});
