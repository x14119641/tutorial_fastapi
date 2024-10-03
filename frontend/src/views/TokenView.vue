<template>
    <div>
        <h1>Your Token: {{ token }}</h1>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'TokenView',
    computed: {
        ...mapGetters(['token']), // Ensure this matches the getter name
    },
    created() {
        console.log("Token in tokenView:", this.token); // Log the token
    }
};
</script>