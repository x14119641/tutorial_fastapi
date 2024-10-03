<template>
    <div :class="{ 'dark': isDarkMode }">
      <button @click="toggleDarkMode">Toggle Dark Mode</button>
      <!-- Other content goes here -->
    </div>
  </template>
  
  <script>
  import { useDarkModeStore } from '@/store/darkModeStore';
  
  export default {
    name: 'DarkModeToggleComponent',
    setup() {
      const darkModeStore = useDarkModeStore();
      
      return {
        isDarkMode: darkModeStore.isDarkMode,
        toggleDarkMode: darkModeStore.toggleDarkMode,
      };
    },
  };
  </script>
  