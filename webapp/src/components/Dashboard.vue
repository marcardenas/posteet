<template>
  <div class="dashboard">
    <h2>Panel de usuario</h2>
    <p>Bienvenido, <strong>{{ email }}</strong></p>
    <div class="actions">
      <button @click="$emit('logout')">Cerrar sesión</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ email: { type: String, required: true } })
</script>

<style scoped>
.dashboard{padding:1rem}
.actions{margin-top:0.8rem}
</style>
