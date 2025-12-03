<template>
    <div class="dashboard-wrapper">
        <button type="button" class="fab" @click="addPostit"><span class="fab-sign">+</span></button>
        <button type="button" class="fab fab-logout" @click="$emit('logout')">
            <span class="fab-sign fab-sign-x">×</span>
        </button>

        <div class="dashboard-content">
            <h2 class="dashboard-title">Panel de {{ email }}</h2>

            <!-- render postits -->
            <Postit v-for="(p, idx) in postits" :key="p.id" :id="p.id" :text="p.text" :left="p.left" :top="p.top"
                :autofocus="p.autofocus" @update="updatePostit" @remove="removePostit" @move="onMove" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Postit from './Postit.vue'
const props = defineProps({ email: { type: String, required: true } })
const emit = defineEmits(['logout'])

const STORAGE_KEY = 'posteet_postits'
const postits = ref([])

function loadPostits() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY)
        if (raw) {
            const parsed = JSON.parse(raw)
            postits.value = parsed.map(p => ({ id: p.id, text: p.text || '', left: (p.left == null ? 60 : p.left), top: (p.top == null ? 100 : p.top) }))
        }
    } catch (e) { console.warn('failed to load postits', e) }
}

function savePostits() {
    try {
        // avoid persisting transient fields like autofocus
        const sanitized = postits.value.map(p => ({ id: p.id, text: p.text, left: p.left, top: p.top }))
        localStorage.setItem(STORAGE_KEY, JSON.stringify(sanitized))
    } catch (e) { console.warn('failed to save postits', e) }
}

let nextId = 1
function ensureNextId() {
    const max = postits.value.reduce((m, p) => Math.max(m, p.id || 0), 0)
    nextId = max + 1
}

onMounted(() => { loadPostits(); ensureNextId() })

function addPostit() {
    const p = { id: nextId++, text: 'Nueva nota', left: 60, top: 100, autofocus: true }
    postits.value.push(p)
    savePostits()
}

function updatePostit({ id, text }) {
    const idx = postits.value.findIndex(p => p.id === id)
    if (idx !== -1) { postits.value[idx].text = text; savePostits() }
}

function removePostit(id) {
    const idx = postits.value.findIndex(p => p.id === id)
    if (idx !== -1) { postits.value.splice(idx, 1); savePostits() }
}

function onMove({ id, left, top }) {
    const idx = postits.value.findIndex(p => p.id === id)
    if (idx !== -1) { postits.value[idx].left = left; postits.value[idx].top = top; savePostits() }
}
</script>

<style scoped>
.dashboard-wrapper {
    position: relative;
    min-height: 60vh
}

.fab {
    position: absolute;
    right: 18px;
    top: 18px;
    background: #ffdd57;
    border: none;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    cursor: pointer;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform .12s ease, box-shadow .12s ease;
    z-index: 1000;
    pointer-events: auto;
    padding: 0
}

.fab:hover {
    transform: translateY(-3px) scale(1.04);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22)
}

.fab:active {
    transform: translateY(-1px) scale(0.99)
}

.fab {
    font-size: 22px;
    font-weight: 800;
    line-height: 1
}

.fab:focus {
    outline: 3px solid rgba(0, 0, 0, 0.08);
    outline-offset: 4px
}

/* plus sign - white fill with black stroke */
.fab-sign {
    display: inline-flex;
    color: #fff;
    font-weight: 900;
    font-size: 24px;
    line-height: 1;
    transform: translateY(-0.6px);
}

.fab-sign::selection {
    background: transparent
}

.fab-logout{
    left: 18px;
    right: auto;
    background: #b33b3b; /* warmer red that pairs with corkboard */
    box-shadow: 0 6px 16px rgba(0,0,0,0.28);
}
.fab-logout:hover{ box-shadow:0 12px 34px rgba(0,0,0,0.34); transform: translateY(-3px) scale(1.04) }
.fab-sign-x{ font-size:22px; transform: translateY(-0.4px) }

.board {
    position: relative;
    min-height: 520px;
    padding: 24px
}

.board-header {
    display: flex;
    justify-content: space-between;
    align-items: center
}

.board-header h2 {
    margin: 0
}

.actions button {
    background: transparent;
    border: none;
    color: var(--accent);
    cursor: pointer
}
</style>
