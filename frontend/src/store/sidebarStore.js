import { defineStore } from 'pinia';

export const useSidebarStore = defineStore('sidebarStore', {
  state: () => ({
    sidebarOpen: true,
  }),
  actions: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    setSidebarOpen(value) {
      this.sidebarOpen = value;
    },
  },
  getters: {
    isSidebarOpen: (state) => state.sidebarOpen,
  },
});
