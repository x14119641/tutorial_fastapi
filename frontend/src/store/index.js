// store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    darkMode: false,
    sidebarOpen: true, // Add sidebar state if needed
  },
  mutations: {
    toggleDarkMode(state) {
      state.darkMode = !state.darkMode;
    },
    toggleSidebar(state) {
      state.sidebarOpen = !state.sidebarOpen;
    },
  },
  getters: {
    darkMode: (state) => state.darkMode,
    sidebarOpen: (state) => state.sidebarOpen,
  },
});
