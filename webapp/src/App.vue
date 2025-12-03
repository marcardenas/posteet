<template>
    <div class="container">
        <main class="postit">
            <h1>{{ mode === 'login' ? 'Iniciar sesión' : 'Registro' }}</h1>

            <form @submit.prevent="onSubmit" class="login-form">
                <label>
                    Usuario
                    <input v-model="form.username" type="text" placeholder="tu.usuario" required />
                </label>

                <label v-if="mode === 'register'">
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

            <p class="hint">Este es un frontend de ejemplo. Conecta el `api/` cuando estés listo.</p>
            <pre v-if="result" class="result">{{ result }}</pre>
        </main>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const mode = ref('login')
const form = reactive({ username: '', email: '', password: '', confirm: '' })
const result = ref('')
const endpoint = ref(import.meta.env.VITE_API_URL ?? 'http://localhost:8000')

function onSubmit() {
    if (mode.value === 'register') {
        if (form.password !== form.confirm) {
            result.value = 'Error: las contraseñas no coinciden.'
            return
        }
        result.value = JSON.stringify({
            message: 'Simulación de registro — conecta el API para funcionamiento real',
            payload: { username: form.username, email: form.email }
        }, null, 2)
        form.password = ''
        form.confirm = ''
    } else {
        result.value = JSON.stringify({
            message: 'Simulación de login — conecta el API para funcionamiento real',
            payload: { username: form.username }
        }, null, 2)
        form.password = ''
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
</style>
