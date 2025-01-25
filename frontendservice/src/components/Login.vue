<template>
  <AuthForm :is-login="true"  @auth-success="handleAuthSuccess" @toggle-form="$emit('toggle-form')" />
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
