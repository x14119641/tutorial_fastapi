<template>
    <div>
        <h1>User Info</h1>
        <p v-if="user">{{ user }}</p>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
    name: 'WhoamiComponent',
    data() {
        return {
            user: null,
        };
    },
    computed: {
        ...mapGetters(['token']), // Use the getter directly
    },
    created() {
        console.log("Token in WhoamiComponent:", this.token); // Log the token

        if (this.token) {
            axios({
                url: '/users/whoami',
                method: 'GET',
                headers: {
                    Authorization: `${this.token}`,
                },
            })
                .then(response => {
                    this.user = response.data; // Handle user data
                })
                .catch(error => {
                    console.error("Error fetching user data:", error.response ? error.response.data : error);
                });
        } else {
            this.$router.push('/login'); // Redirect to login if no token
        }
    },

};
</script>