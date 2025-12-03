<template>
  <div class="auth-card">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="submit" class="login-form">
      <label>
        Correo
        <input v-model="email" type="email" placeholder="tu@email.com" required />
      </label>
      <label>
        Contraseña
        <input v-model="password" type="password" placeholder="••••••" required />
      </label>
      <div class="actions">
        <button type="submit">Entrar</button>
        <button type="button" class="ghost" @click="$emit('switch','register')">Registrarse</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['login-success','notify','switch'])

const email = ref('')
const password = ref('')
const endpoint = import.meta.env.VITE_API_URL || 'http://localhost:8080'

function isValidEmail(e){
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)
}

function submit(){
  if(!isValidEmail(email.value)){
    emit('notify',{type:'error',message:'Correo inválido'})
    return
  }
  if(!password.value){
    emit('notify',{type:'error',message:'Contraseña vacía'})
    return
  }

  const url = `${endpoint}/auth/jwt/login`
  const payload = new URLSearchParams({ username: email.value, password: password.value })
  axios.post(url, payload)
    .then(res => {
      emit('notify',{type:'success',message:'Inicio de sesión correcto'})
      emit('login-success',{email: email.value, data: res.data})
    })
    .catch(err => {
      const msg = err.response && err.response.data ? (err.response.data.detail || JSON.stringify(err.response.data)) : err.message
      emit('notify',{type:'error',message: 'Error en login: '+msg})
    })
}
</script>

<style scoped>
.auth-card{padding:0.5rem}
.actions{display:flex;gap:0.5rem;margin-top:0.5rem}
.ghost{background:transparent;border:none;color:var(--accent);cursor:pointer}
</style>
