<template>
    <aside :class="['transition-width duration-300', sidebarOpen ? 'w-64' : 'w-20', darkMode ? 'bg-gray-800 text-white' : 'bg-gray-300 text-black']">
      <div class="p-4 flex justify-between">
        <h2 class="text-lg" v-if="sidebarOpen">Menu</h2>
        <button @click="toggleSidebar" class="focus:outline-none">
          <svg v-if="!sidebarOpen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
            stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
            class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <nav class="p-4">
        <ul>
          <li class="mb-4">
            <a href="#" class="text-lg" :class="{ 'hidden': !sidebarOpen }">Dashboard</a>
          </li>
          <li class="mb-4">
            <a href="#" class="text-lg" :class="{ 'hidden': !sidebarOpen }">Profile</a>
          </li>
          <li>
            <a href="#" class="text-lg" :class="{ 'hidden': !sidebarOpen }">Settings</a>
          </li>
        </ul>
      </nav>
    </aside>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';
  
  export default {
    name: 'SidebarComponent',
    computed: {
      ...mapGetters(['darkMode', 'sidebarOpen']), // Access darkMode and sidebarOpen via Vuex getters
    },
    methods: {
      toggleSidebar() {
        this.$store.commit('toggleSidebar'); // Commit the mutation to toggle sidebar
      }
    }
  };
  </script>
  
  <style scoped>
  .transition-width {
    transition-property: width;
  }
  </style>
  