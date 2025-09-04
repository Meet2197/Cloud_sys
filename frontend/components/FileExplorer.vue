<template>
  <div class="card p-3">
    <div class="flex items-center gap-2 mb-2">
      <button class="btn" @click="view='grid'" :class="{ 'bg-accent/30': view==='grid' }">Grid</button>
      <button class="btn" @click="view='list'" :class="{ 'bg-accent/30': view==='list' }">List</button>
      <select v-model="filterKind" class="bg-white/10 rounded-xl2 px-2 py-1">
        <option value="">All</option>
        <option>image</option>
        <option>text</option>
        <option>video</option>
      </select>
      <select v-model.number="filterCluster" class="bg-white/10 rounded-xl2 px-2 py-1">
        <option :value="undefined">Cluster: Any</option>
        <option v-for="c in clusterIds" :key="c" :value="c">Cluster {{ c }}</option>
      </select>
    </div>

    <div v-if="view==='grid'" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      <FileCard v-for="f in files" :key="f.id" :name="f.name" :size="f.size" :kind="f.kind" @select="select(f)" @ctx="openMenu($event, f)" />
    </div>

    <table v-else class="w-full text-sm">
      <thead class="opacity-50">
        <tr>
          <th class="text-left px-3 py-2">Name</th>
          <th class="text-left px-3 py-2">Type</th>
          <th class="text-right px-3 py-2">Size</th>
        </tr>
      </thead>
      <tbody>
        <FileListRow v-for="f in files" :key="f.id" :name="f.name" :size="f.size" :kind="f.kind" @ctx="openMenu($event, f)" @click="select(f)" />
      </tbody>
    </table>

    <div v-if="menu.visible" class="fixed z-50" :style="{ left: menu.x+'px', top: menu.y+'px' }" @click.stop>
      <div class="card min-w-[180px] p-2 space-y-1">
        <button class="w-full text-left hover:bg-white/5 rounded px-2 py-1" @click="download(menu.file)">Download</button>
        <button class="w-full text-left hover:bg-white/5 rounded px-2 py-1" @click="emit('delete', menu.file)">Delete</button>
        <button class="w-full text-left hover:bg-white/5 rounded px-2 py-1" @click="emit('share', menu.file)">Share</button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import FileCard from './FileCard.vue'
import FileListRow from './FileListRow.vue'
const props = defineProps<{ q: string }>()
const emit = defineEmits(['select','delete','share'])
const { listFiles, download: dl, getClusters } = useApi()
const files = ref<any[]>([])
const view = ref<'grid'|'list'>('grid')
const filterKind = ref('')
const filterCluster = ref<number | undefined>(undefined)
const clusterIds = ref<number[]>([])

async function load() {
  const data = await listFiles({ q: props.q || undefined, kind: filterKind.value || undefined, cluster_id: filterCluster.value })
  files.value = data
}
watch([() => props.q, filterKind, filterCluster], load, { immediate: true })

onMounted(async () => {
  const g = await getClusters();
  clusterIds.value = Array.from(new Set(g.nodes.map((n:any) => n.cluster).filter((x:number)=>x>=0)))
})

const select = (f:any) => emit('select', f)
const download = (f:any) => dl(f.id)

const menu = reactive({ visible:false, x:0, y:0, file: null as any })
function openMenu(e: MouseEvent, f:any){
  menu.visible = true; menu.x = e.clientX; menu.y = e.clientY; menu.file = f
  const close = () => { menu.visible = false; window.removeEventListener('click', close) }
  window.addEventListener('click', close)
}
</script>
