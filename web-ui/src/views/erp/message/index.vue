<template>
    <div>
        <div v-if="messages.length > 0" v-for="message in messages" :key="message">{{ message }}</div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                messages: [],
                socket: null,
                // 新增后端需要的参数
                chatId: '',
                baseUrl: ''
            };
        },
        mounted() {
            this.initWebSocket();
        },
        methods: {
            initWebSocket() {
                // 传递后端需要的参数
                this.socket = new WebSocket(`ws://127.0.0.1:9080/chat?chatId=``{this.chatId}&baseUrl=``{this.baseUrl}`);
                this.socket.onmessage = event => {
                    this.messages.push(event.data);
                };
            }
        }
    };
</script>