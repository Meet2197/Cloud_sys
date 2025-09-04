<template>
  <header class="card w-full p-3 flex items-center gap-3 sticky top-0 z-20">
    <div class="font-semibold text-lg">☁️ Cloud</div>
    <div class="flex-1"></div>
    <div class="relative w-full max-w-xl">
      <input v-model="q" @input="onInput" placeholder="Search files…" class="w-full bg-white/5 rounded-xl2 px-4 py-2 outline-none" />
      <div v-if="suggestions.length" class="absolute mt-1 card w-full p-2 space-y-1">
        <button v-for="s in suggestions" :key="s" class="w-full text-left hover:bg-white/5 rounded px-2 py-1" @click="applySuggestion(s)">{{ s }}</button>
      </div>
    </div>
    <div class="flex gap-2">
      <button class="btn" @click="$emit('new-folder')">New Folder</button>
      <label class="btn cursor-pointer">
        Upload
        <input type="file" class="hidden" multiple @change="onUpload">
      </label>
    </div>
  </header>
</template>
<script setup lang="ts">
const emit = defineEmits(['search','new-folder','upload'])
const q = ref('')
const suggestions = ref<string[]>([])
let t: any
const onInput = () => {
  clearTimeout(t)
  t = setTimeout(() => {
    suggestions.value = q.value.length > 1 ? [q.value, q.value + ' report', 'tag:' + q.value] : []
    emit('search', q.value)
  }, 250)
}
const applySuggestion = (s: string) => { q.value = s; suggestions.value = []; emit('search', q.value) }
const onUpload = (e: any) => emit('upload', Array.from(e.target.files || []))
</script>
