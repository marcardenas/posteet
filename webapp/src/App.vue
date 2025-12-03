<template>
  <div class="container">
    <main>
      <h1>Iniciar sesión</h1>
      <form @submit.prevent="onSubmit" class="login-form">
        <label>
          Usuario
          <input v-model="form.username" type="text" placeholder="tu.usuario" required />
        </label>
        <label>
          Contraseña
          <input v-model="form.password" type="password" placeholder="••••••" required />
        </label>
        <button type="submit">Entrar</button>
      </form>
      <p class="hint">Este es un frontend de ejemplo. Conecta el `api/` cuando estés listo.</p>
      <pre v-if="result" class="result">{{ result }}</pre>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const form = reactive({ username: '', password: '' })
const result = ref('')

function onSubmit() {
  // Simulación local; conecta la lógica con tu API en `api/`.
  result.value = JSON.stringify({
    message: 'Simulación de login — conecta el API para funcionamiento real',
    payload: { username: form.username }
  }, null, 2)
  form.password = ''
}
</script>

<style scoped>
/* keep minimal spacing here; actual styles in src/styles.css */
</style>
