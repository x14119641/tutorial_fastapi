export default {
  state: {
    darkMode: false,
  },
  mutations: {
    toggleDarkMode(state) {
      state.darkMode = !state.darkMode;
    },
  },
  getters: {
    darkMode: (state) => state.darkMode,
  },
};
 