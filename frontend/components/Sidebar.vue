<template>
  <aside class="card w-64 p-4 hidden lg:block">
    <nav class="space-y-1">
      <button class="btn w-full justify-start" :class="{ 'bg-accent/30': active==='dashboard' }" @click="$emit('nav','dashboard')">Dashboard</button>
      <button class="btn w-full justify-start" :class="{ 'bg-accent/30': active==='files' }" @click="$emit('nav','files')">My Files</button>
      <button class="btn w-full justify-start" @click="$emit('nav','shared')">Shared with Me</button>
      <button class="btn w-full justify-start" :class="{ 'bg-accent/30': active==='analytics' }" @click="$emit('nav','analytics')">Analytics</button>
      <button class="btn w-full justify-start" @click="$emit('nav','settings')">Settings</button>
    </nav>
  </aside>
</template>
<script setup lang="ts">
defineProps<{ active: string }>()
</script>
