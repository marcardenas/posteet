<template>
  <div class="auth-card">
    <h2>Registro</h2>
    <form @submit.prevent="submit" class="login-form">
      <label>
        Correo
        <input v-model="email" type="email" placeholder="tu@email.com" required />
      </label>
      <label>
        Contraseña
        <input v-model="password" type="password" placeholder="••••••" required />
      </label>
      <label>
        Repetir contraseña
        <input v-model="confirm" type="password" placeholder="••••••" required />
      </label>
      <div class="actions">
        <button type="submit">Registrarse</button>
        <button type="button" class="ghost" @click="$emit('switch','login')">Volver a login</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['register-success','notify','switch'])

const email = ref('')
const password = ref('')
const confirm = ref('')
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
  if(password.value !== confirm.value){
    emit('notify',{type:'error',message:'Las contraseñas no coinciden'})
    return
  }

  // Perform registration request to backend
  const url = `${endpoint}/auth/register`
  axios.post(url,{ email: email.value, password: password.value })
    .then(res => {
      emit('notify',{type:'success',message:'Registro exitoso'})
      emit('register-success',{email: email.value})
    })
    .catch(err => {
      const msg = err.response && err.response.data ? (err.response.data.detail || JSON.stringify(err.response.data)) : err.message
      emit('notify',{type:'error',message: 'Registro falló: '+msg})
    })
}
</script>

<style scoped>
.actions{display:flex;gap:0.5rem;margin-top:0.5rem}
.ghost{background:transparent;border:none;color:var(--accent);cursor:pointer}
</style>
