<template>
    <div>
      <h1>User Info</h1>
      <p v-if="user">{{ user }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useTokenStore } from '@/store/tokenStore';
  
  export default {
    name: 'WhoamiComponent',
    data() {
      return {
        user: null,
      };
    },
    created() {
      const tokenStore = useTokenStore();
      if (tokenStore.getToken) {
        axios({
          url: '/users/whoami',
          method: 'GET',
          headers: {
            Authorization: tokenStore.getToken,
          },
        })
          .then(response => {
            this.user = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      } else {
        this.$router.push('/login');
      }
    },
  };
  </script>
  