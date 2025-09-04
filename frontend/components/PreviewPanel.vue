<template>
  <div class="card p-4 h-full">
    <div v-if="!file">Select a file to preview</div>
    <template v-else>
      <h3 class="font-semibold mb-3">{{ file.name }}</h3>
      <div v-if="file.mime_type?.startsWith('image/')" class="rounded-xl2 overflow-hidden">
        <img :src="imgUrl" class="w-full"/>
      </div>
      <div v-else-if="file.mime_type?.startsWith('text/')" class="bg-black/40 p-3 rounded-xl2 text-sm whitespace-pre-wrap">(Text preview not implemented – download)</div>
      <div v-else class="opacity-70">No preview. Use download.</div>
      <div class="mt-3 flex gap-2">
        <button class="btn" @click="download">Download</button>
        <button class="btn" @click="$emit('delete')">Delete</button>
      </div>
      <div v-if="ndPyramid?.length" class="mt-4 space-y-2">
        <div class="font-semibold">N‑D Resolution Pyramid</div>
        <input type="range" min="0" :max="ndPyramid.length-1" v-model.number="level"/>
        <div class="text-xs opacity-70">Level: {{ level }}</div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ file: any | null }>()
const config = useRuntimeConfig()
const imgUrl = computed(() => props.file ? `${config.public.apiBase}/files/${props.file.id}/download` : '')
const ndPyramid = computed(() => props.file?.metadata?.nd_pyramid || [])
const level = ref(0)
const emit = defineEmits(['delete'])
const download = () => window.location.href = imgUrl.value
</script>
