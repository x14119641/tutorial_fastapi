export default {
  state: {
    sidebarOpen: true,
  },
  mutations: {
    toggleSidebar(state) {
      state.sidebarOpen = !state.sidebarOpen;
    },
  },
  getters: {
    sidebarOpen: (state) => state.sidebarOpen,
  },
}; 
