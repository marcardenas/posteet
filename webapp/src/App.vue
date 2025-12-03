<template>
  <div class="container">
    <main class="postit">
      <component :is="currentView"
             v-on:login-success="onLoginSuccess"
             v-on:register-success="onRegisterSuccess"
             v-on:notify="handleNotify"
             v-on:switch="setMode"
             v-on:logout="logout"
             v-bind="componentProps"
      />

      <!-- Toast notifications -->
      <div class="toasts" aria-live="polite">
        <div v-for="t in toasts" :key="t.id" :class="['toast', t.type]">
          <div class="toast-body">
            <strong v-if="t.type === 'success'">OK</strong>
            <strong v-else>Error</strong>
            <span class="msg">{{ t.message }}</span>
          </div>
          <button class="close" @click="removeToast(t.id)">×</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Dashboard from './components/Dashboard.vue'

const mode = ref('login')
const isAuthenticated = ref(false)
const userEmail = ref('')
const result = ref('')

// load persisted user
if (localStorage.getItem('posteet_user')){
  try{ const u = JSON.parse(localStorage.getItem('posteet_user'))
    userEmail.value = u.email || ''
    isAuthenticated.value = !!userEmail.value
  }catch(e){/* ignore */}
}

const currentView = computed(() => {
  if (isAuthenticated.value) return Dashboard
  return mode.value === 'login' ? Login : Register
})

const componentProps = computed(() => {
  return isAuthenticated.value ? { email: userEmail.value } : {}
})

// simple toast notifications
const toasts = ref([])
let nextToastId = 1
function addToast(type, message, timeout = 4000) {
  const id = nextToastId++
  toasts.value.push({ id, type, message })
  if (timeout > 0) setTimeout(() => removeToast(id), timeout)
}
function removeToast(id) {
  const i = toasts.value.findIndex(t => t.id === id)
  if (i !== -1) toasts.value.splice(i, 1)
}

function handleNotify(payload){
  if(payload && payload.type && payload.message) addToast(payload.type, payload.message)
}

function onRegisterSuccess(payload){
  // payload: { email }
  userEmail.value = payload.email
  isAuthenticated.value = true
  localStorage.setItem('posteet_user', JSON.stringify({ email: payload.email }))
}

function onLoginSuccess(payload){
  userEmail.value = payload.email
  isAuthenticated.value = true
  localStorage.setItem('posteet_user', JSON.stringify({ email: payload.email }))
}

function logout(){
  isAuthenticated.value = false
  userEmail.value = ''
  localStorage.removeItem('posteet_user')
  mode.value = 'login'
}

function setMode(m){ mode.value = m }
</script>

<style scoped>
/* Scoped minimal overrides; the main design is in src/styles.css */
.actions {
  margin-top: 0.8rem
}

.ghost {
  background: transparent;
  border: none;
  color: var(--accent);
  cursor: pointer;
  font-weight: 600
}

/* Toasts */
.toasts {
  position: fixed;
  right: 20px;
  top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
}

.toast {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 8px;
  padding: 8px 12px;
  min-width: 220px;
  box-shadow: 0 8px 20px rgba(2, 6, 23, 0.2);
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.toast.success {
  border-left: 4px solid #16a34a
}

.toast.error {
  border-left: 4px solid #dc2626
}

.toast .msg {
  margin-left: 8px;
  font-size: 0.95rem
}

.toast .close {
  margin-left: auto;
  background: transparent;
  border: none;
  font-size: 16px;
  cursor: pointer
}
</style>
