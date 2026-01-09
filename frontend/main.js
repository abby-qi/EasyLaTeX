const { createApp } = require('vue');
const MainPage = require('./pages/MainPage.vue').default;

const app = createApp(MainPage);

app.mount('#app');