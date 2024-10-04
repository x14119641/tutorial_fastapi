<template>
    <div>
      <h1>Your Token: {{ token }}</h1>
    </div>
  </template>
  
  <script>
  import { useTokenStore } from '@/store/tokenStore';
  
  export default {
    setup() {
      const store = useTokenStore();
  
      return {
        token: store.token,
      };
    },
  };
  </script>
  