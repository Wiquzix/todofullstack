import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router';
import Register from './components/Register.vue';
import Login from './components/Login.vue';
import Tasks from "./components/Tasks.vue";
const routes = [
    { path: '/register', component: Register },
    { path: '/login', component: Login },
    { path: '/tasks', component: Tasks}
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
