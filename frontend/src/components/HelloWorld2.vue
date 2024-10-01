<template>
    <h2 class="text-2xl font-bold mb-6">{{ title }}</h2>

    <div class="bg-blue-500 p-4 text-white rounded">
        <h1 class="text-2xl font-bold">Hello Tailwind CSS!</h1>
        <p>This is a Vue component styled with Tailwind CSS.</p>
        <p> Message: {{ msg }}</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'PingComponent',
    data() {
        return {
            title: 'My Title',
            msg: ''
        }
    },
    methods: {
        getMessage() {
            axios.get('/hello')
                .then((res) => {
                    this.msg = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    },
    created() {
        this.getMessage()
    }
}
</script>
