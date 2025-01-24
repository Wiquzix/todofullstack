<template>
  <AuthForm :is-login="false" @toggle-form="$emit('toggle-form')" @auth-success="handleAuthSuccess" />
</template>

<script>
import AuthForm from './AuthForm.vue';
export default {
  components: {
    AuthForm,
  },
  emits: ['toggle-form'],
  setup(props, {emit}) {
      const handleAuthSuccess = () => {
        emit('toggle-form')
      }
      return {handleAuthSuccess}
  },
};
</script>
