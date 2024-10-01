<template>
  <div :class="darkMode ? 'bg-gray-900 text-white' : 'bg-gray-200 text-black'" class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="p-4 flex items-center justify-between" :class="darkMode ? 'bg-gray-800' : 'bg-gray-300'">
      <div class="flex items-center">
        <!-- Logo -->
        <img src="@/assets/logo.png" alt="Logo" class="w-10 h-10 mr-4">
        <h1 class="text-xl">Just Playing Around</h1>
      </div>
      <div class="flex items-center">
        <!-- Dark Mode Toggle Button -->
        <button @click="toggleDarkMode" class="p-2 rounded hover:bg-gray-400">
          <span v-if="darkMode">🌙</span>
          <span v-else>☀️</span>
        </button>
        <Button icon="pi pi-bars" class="p-button-text ml-2" @click="toggleSidebar" />
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex flex-1">
      <!-- Sidebar -->
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

      <!-- Main Content Area -->
      <main class="flex-1 p-6">
        <router-view></router-view>
      </main>
    </div>

    <!-- Footer -->
    <footer :class="darkMode ? 'bg-gray-800 text-white' : 'bg-gray-300 text-black'" class="p-4 text-center">
      <p>&copy; 2024 My App. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sidebarOpen: true,
      darkMode: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
  },
};
</script>

<style scoped>
/* Transition width smoothly */
.transition-width {
  transition-property: width;
}
</style>
