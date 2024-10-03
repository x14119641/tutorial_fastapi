<template>
  <div :class="darkMode ? 'bg-gray-900 text-white' : 'bg-gray-200 text-black'" class="min-h-screen flex flex-col">
    <header class="p-4 flex items-center justify-between" :class="darkMode ? 'bg-gray-800' : 'bg-gray-300'">
      <div class="flex items-center">
        <h1 class="text-xl">My App</h1>
        <button @click="toggleDarkMode" class="p-2 rounded hover:bg-gray-400">
          <span v-if="darkMode">🌙</span>
          <span v-else>☀️</span>
        </button>
      </div>
    </header>

    <div class="flex flex-1">
      <SidebarComponent />
      <RouterView></RouterView>
    </div>

    <footer :class="darkMode ? 'bg-gray-800 text-white' : 'bg-gray-300 text-black'" class="p-4 text-center">
      <p>&copy; 2024 My App. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import SidebarComponent from './SidebarComponent.vue';

export default {
  components: {
    SidebarComponent,
  },
  computed: {
    ...mapGetters(['darkMode', 'sidebarOpen']), // Access darkMode and sidebarOpen from Vuex
  },
  methods: {
    toggleDarkMode() {
      this.$store.commit('toggleDarkMode'); // Commit the mutation to toggle dark mode
    }
  }
};
</script>
