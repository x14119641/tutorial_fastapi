import { defineStore } from 'pinia';

export const useDarkModeStore = defineStore('darkModeStore', {
  state: () => ({
    darkMode: false,
  }),
  actions: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
    setDarkMode(value) {
      this.darkMode = value;
    },
  },
  getters: {
    isDarkMode: (state) => state.darkMode,
  },
});
