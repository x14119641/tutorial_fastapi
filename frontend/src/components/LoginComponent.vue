<template>
  <div class="flex flex-col items-center justify-center flex-grow">
    <div :class="darkMode ? 'bg-gray-800 text-white' : 'bg-white text-black'" class="p-8 rounded-lg shadow-lg w-full max-w-sm">
      <h2 class="text-2xl font-bold text-center mb-6">{{ title }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label for="usernameOrEmail" class="block mb-2">Username or Email</label>
          <input type="text" id="usernameOrEmail" v-model="usernameOrEmail" required class="w-full p-2 border rounded" />
        </div>

        <div class="mb-4">
          <label for="password" class="block mb-2">Password</label>
          <input type="password" id="password" v-model="password" required class="w-full p-2 border rounded" />
        </div>

        <button type="submit"
          class="w-full p-2 bg-blue-600 text-white rounded hover:bg-blue-500 transition duration-300">
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'LoginComponent',
  computed: {
    ...mapGetters(['darkMode']), // Access darkMode via Vuex getter
  },
  data() {
    return {
      title: 'Login',
      usernameOrEmail: '', // Single data property for username or email
      password: ''
    };
  },
  methods: {
    handleSubmit() {
      // Handle login logic here
      console.log(`Username or Email: ${this.usernameOrEmail}, Password: ${this.password}`);
    }
  }
};
</script>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
</style>
