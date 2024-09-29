<template>
  <div>
    <p>The message : {{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'PingComponent',
    data() {
        return {
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
