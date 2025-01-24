<template>
    <div class="container">
        <h1>Задачи</h1>
        <p>Тут будут ваши задачи.</p>
        <button @click="redirectToLogin">Войти</button>
        <button @click="redirectToRegister">Регистрация</button>
    </div>
</template>

<script>
import { useRouter } from 'vue-router';
    export default {
        setup() {
            const router = useRouter()
            const redirectToLogin = () => {
                router.push('/login')
            }
             const redirectToRegister = () => {
                router.push('/register')
            }
            return {
                redirectToLogin,
                redirectToRegister,
            }
        }
    }
</script>
