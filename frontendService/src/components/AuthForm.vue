<template>
  <div class="auth-form">
    <h2>{{ isLogin ? "Вход" : "Регистрация" }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">Имя пользователя</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Пароль</label>
        <input type="password" id="password" v-model="password" required>
      </div>
        <button type="submit">{{ isLogin ? "Войти" : "Зарегистрироваться" }}</button>
       <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
    <p>
        <button @click="$emit('toggle-form')">
            {{ isLogin ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти' }}
        </button>
    </p>
  </div>
</template>

<script>
import axios from "axios";
import {ref} from "vue";
import { useRouter } from 'vue-router';
export default {
  props: {
      isLogin: {
          type: Boolean,
          default: true,
      },
    onAuthSuccess: {
      type: Function,
      default: () => { },
    },
  },
    emits:['toggle-form'],
  setup(props, { emit }) {
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();
    const handleSubmit = async () => {
      try {
        let response
        if (props.isLogin) {
            response = await axios.post(
                "http://localhost:8001/login",
                { username: username.value, password: password.value }
            );
        } else {
            response = await axios.post(
                "http://localhost:8001/users",
                { username: username.value, password: password.value }
            );
        }

          if (response.status === 200) {
              if(props.isLogin) {
                localStorage.setItem("token", response.data.access_token);
                router.push("/tasks");
            }
             else {
                 router.push("/login");
            }
          }
          else {
              errorMessage.value = response.data.detail || "Ошибка аутентификации"
              console.error("Error authenticating user:", response);
          }
      } catch (error) {
          errorMessage.value = error.response?.data?.detail || "Ошибка аутентификации";
          console.error("Error authenticating user:", error);
      }
    };

    return {
      username,
      password,
        errorMessage,
      handleSubmit,
    };
  },
};
</script>
