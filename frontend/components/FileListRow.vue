<template>
  <tr @contextmenu.prevent="$emit('ctx')" class="hover:bg-white/5">
    <td class="px-3 py-2">{{ name }}</td>
    <td class="px-3 py-2">{{ kind }}</td>
    <td class="px-3 py-2 text-right">{{ sizeKB }} KB</td>
  </tr>
</template>
<script setup lang="ts">
const props = defineProps<{ name: string, size: number, kind: string }>()
const sizeKB = computed(() => Math.ceil((props.size||0)/1024))
</script>
