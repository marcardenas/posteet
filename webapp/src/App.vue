<template>
    <div class="container">
        <main class="postit">
            <h1>{{ mode === 'login' ? 'Iniciar sesión' : 'Registro' }}</h1>

            <form @submit.prevent="onSubmit" class="login-form">
                <label>
                    Correo
                    <input v-model="form.email" type="email" placeholder="tu@email.com" required />
                </label>

                <label>
                    Contraseña
                    <input v-model="form.password" type="password" placeholder="••••••" required />
                </label>

                <label v-if="mode === 'register'">
                    Repetir contraseña
                    <input v-model="form.confirm" type="password" placeholder="••••••" required />
                </label>

                <button type="submit">{{ mode === 'login' ? 'Entrar' : 'Registrarse' }}</button>
            </form>

            <div class="actions">
                <button class="ghost" @click="toggleMode">
                    {{ mode === 'login' ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión' }}
                </button>
            </div>

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
import { reactive, ref } from 'vue'
import axios from 'axios'

const mode = ref('login')
const form = reactive({ email: '', password: '', confirm: '' })
const result = ref('')
const endpoint = ref(import.meta.env.VITE_API_URL ?? 'http://localhost:8000')

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

// simple validators
function isValidEmail(email) {
    // Basic RFC-ish check: something@something.tld (no spaces)
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function onSubmit() {
    if (mode.value === 'register') {
        // validate email format
        if (!isValidEmail(form.email)) {
            addToast('error', 'Correo inválido. Usa el formato usuario@dominio.ext')
            result.value = 'Error: correo inválido'
            return
        }

        // validate passwords
        if (!form.password) {
            addToast('error', 'La contraseña no puede estar vacía')
            result.value = 'Error: contraseña vacía'
            return
        }
        if (form.password !== form.confirm) {
            addToast('error', 'Las contraseñas no coinciden')
            result.value = 'Error: las contraseñas no coinciden.'
            return
        }

        const register_endpoint = `${endpoint.value}/auth/register`

        axios.post(register_endpoint, {
            email: form.email,
            password: form.password,
        }).then(response => {
            // success: show toast, clear fields and redirect to home
            addToast('success', 'Registro exitoso. Redirigiendo a inicio...')
            result.value = JSON.stringify({
                message: 'Registro exitoso',
                payload: response.data
            }, null, 2)
            form.password = ''
            form.confirm = ''
            setTimeout(() => { window.location.href = '/' }, 1200)
        }).catch(error => {
            const errMsg = error.response && error.response.data ? (error.response.data.detail || JSON.stringify(error.response.data)) : error.message
            addToast('error', 'Error en el registro: ' + errMsg)
            result.value = JSON.stringify({
                message: 'Error en el registro',
                error: error.response ? error.response.data : error.message
            }, null, 2)
        })
    } else {
        // login: validate email format
        if (!isValidEmail(form.email)) {
            addToast('error', 'Correo inválido. Usa el formato usuario@dominio.ext')
            result.value = 'Error: correo inválido'
            return
        }

        const login_endpoint = `${endpoint.value}/auth/jwt/login`

        axios.post(login_endpoint, new URLSearchParams({
            username: form.email,
            password: form.password,
        }), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).then(response => {
            // success: show toast, clear fields and redirect to home
            addToast('success', 'Inicio de sesión exitoso. Redirigiendo a inicio...')
            result.value = JSON.stringify({
                message: 'Inicio de sesión exitoso',
                payload: response.data
            }, null, 2)
            form.password = ''
            setTimeout(() => { window.location.href = '/' }, 1200)
        }).catch(error => {
            const errMsg = error.response && error.response.data ? (error.response.data.detail || JSON.stringify(error.response.data)) : error.message
            addToast('error', 'Error en el inicio de sesión: ' + errMsg)
            result.value = JSON.stringify({
                message: 'Error en el inicio de sesión',
                error: error.response ? error.response.data : error.message
            }, null, 2)
        })
    }
}

function toggleMode() {
    mode.value = mode.value === 'login' ? 'register' : 'login'
    result.value = ''
}
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
