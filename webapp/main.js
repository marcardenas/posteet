const { createApp, ref } = Vue;

createApp({
  setup() {
    const form = ref({ username: '', password: '' });
    const result = ref('');

    function onSubmit() {
      // Placeholder: user will connect this to the real API.
      console.log('Login attempt', form.value);
      result.value = JSON.stringify({
        message: 'Simulación de login — conecta el API para funcionamiento real',
        payload: { ...form.value },
      }, null, 2);
      // Reset password field for safety in the demo
      form.value.password = '';
    }

    return { form, result, onSubmit };
  }
}).mount('#app');
