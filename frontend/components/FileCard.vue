<template>
  <div class="card p-3 group hover:translate-y-[-2px] transition cursor-pointer" @click="$emit('select')" @contextmenu.prevent="$emit('ctx')">
    <div class="icon mb-2">
      <span v-if="kind==='image'">🖼️</span>
      <span v-else-if="kind==='text'">📄</span>
      <span v-else-if="kind==='video'">🎬</span>
      <span v-else>📦</span>
    </div>
    <div class="text-sm truncate">{{ name }}</div>
    <div class="text-xs opacity-60">{{ sizeKB }} KB</div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ name: string, size: number, kind: string }>()
const sizeKB = computed(() => Math.ceil((props.size||0)/1024))
</script>
