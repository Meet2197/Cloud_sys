<template>
  <div class="card p-3">
    <div class="font-semibold mb-2">Transfers</div>
    <div v-if="!queue.length" class="text-sm opacity-70">No active uploads</div>
    <div v-for="item in queue" :key="item.id" class="mb-2">
      <div class="text-sm">{{ item.file.name }}</div>
      <div class="w-full bg-white/10 h-2 rounded-xl2 overflow-hidden">
        <div class="bg-accent h-2" :style="{ width: item.progress + '%' }"></div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ queue: { id: string, file: File, progress: number }[] }>()
</script>
