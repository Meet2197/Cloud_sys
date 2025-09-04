<template>
  <div class="card p-4 h-full">
    <div class="font-semibold mb-2">Metadata</div>
    <div v-if="!file" class="opacity-70">Select a file</div>
    <template v-else>
      <textarea v-model="jsonStr" class="w-full h-40 bg-black/30 rounded-xl2 p-2 text-sm font-mono"></textarea>
      <input v-model="tags" placeholder="tags (space-separated)" class="mt-2 w-full bg-black/30 rounded-xl2 p-2 text-sm"/>
      <div class="mt-2 flex gap-2">
        <button class="btn" @click="save">Save</button>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ file: any | null }>()
const emit = defineEmits(['saved'])
const jsonStr = ref('')
const tags = ref('')
watch(() => props.file, (f) => {
  jsonStr.value = JSON.stringify(f?.metadata || {}, null, 2)
  tags.value = f?.metadata_tags || ''
}, { immediate: true })
const { updateMetadata } = useApi()
const save = async () => {
  const json = JSON.parse(jsonStr.value || '{}')
  await updateMetadata(props.file.id, { json, tags: tags.value })
  emit('saved')
}
</script>
