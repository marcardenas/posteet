<template>
  <div class="postit-note" :style="noteStyle()" @mousedown.prevent="startDrag" @touchstart.prevent="startDragTouch">
    <textarea ref="ta" v-model="localText" @input="onInput" class="postit-text"></textarea>
    <button class="postit-remove" @click="$emit('remove', id)">×</button>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  id: [String, Number],
  text: { type: String, default: '' },
  left: { type: Number, default: 40 },
  top: { type: Number, default: 80 },
  autofocus: { type: Boolean, default: false }
})
const emit = defineEmits(['update','remove','move'])

const localText = ref(props.text)
const left = ref(props.left)
const top = ref(props.top)
const ta = ref(null)

watch(() => props.text, (v) => { localText.value = v })
watch(() => props.left, (v) => { left.value = v })
watch(() => props.top, (v) => { top.value = v })

onMounted(()=>{
  if(props.autofocus && ta.value){ ta.value.focus(); ta.value.select() }
})

function onInput(){
  emit('update', { id: props.id, text: localText.value })
}

// Dragging
let dragging = false
let startX = 0, startY = 0, startLeft = 0, startTop = 0

function noteStyle(){
  return { left: left.value + 'px', top: top.value + 'px' }
}

function startDrag(e){
  dragging = true
  startX = e.clientX
  startY = e.clientY
  startLeft = left.value
  startTop = top.value
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('mouseup', endDrag)
}

function onDrag(e){
  if(!dragging) return
  const dx = e.clientX - startX
  const dy = e.clientY - startY
  left.value = Math.max(8, startLeft + dx)
  top.value = Math.max(8, startTop + dy)
  emit('move', { id: props.id, left: left.value, top: top.value })
}

function endDrag(){
  dragging = false
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', endDrag)
}

// touch support
function startDragTouch(ev){
  const t = ev.touches[0]
  dragging = true
  startX = t.clientX
  startY = t.clientY
  startLeft = left.value
  startTop = top.value
  window.addEventListener('touchmove', onDragTouch, { passive: false })
  window.addEventListener('touchend', endDragTouch)
}

function onDragTouch(ev){
  ev.preventDefault()
  if(!dragging) return
  const t = ev.touches[0]
  const dx = t.clientX - startX
  const dy = t.clientY - startY
  left.value = Math.max(8, startLeft + dx)
  top.value = Math.max(8, startTop + dy)
  emit('move', { id: props.id, left: left.value, top: top.value })
}

function endDragTouch(){
  dragging = false
  window.removeEventListener('touchmove', onDragTouch)
  window.removeEventListener('touchend', endDragTouch)
}

onBeforeUnmount(()=>{
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', endDrag)
  window.removeEventListener('touchmove', onDragTouch)
  window.removeEventListener('touchend', endDragTouch)
})
</script>

<style scoped>
.postit-note{
  width:160px;
  min-height:140px;
  background:#fff59d;
  padding:10px 8px 8px 10px;
  border-radius:6px;
  box-shadow:0 8px 18px rgba(0,0,0,0.25);
  position:absolute;
  border:1px solid rgba(0,0,0,0.06);
  touch-action: none;
  cursor: grab;
}
.postit-note:active{ cursor:grabbing }
.postit-text{width:100%;height:100%;border:none;background:transparent;resize:none;font-size:14px;outline:none}
.postit-remove{position:absolute;top:6px;right:6px;background:transparent;border:none;font-weight:700;cursor:pointer}
</style>
