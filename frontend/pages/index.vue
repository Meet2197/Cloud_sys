<template>
  <div class="min-h-screen text-white px-3 py-3 lg:px-6">
    <div class="flex gap-3">
      <Sidebar :active="active" @nav="active=$event"/>
      <div class="flex-1 space-y-3">
        <TopBar @search="q=$event" @new-folder="createFolder" @upload="enqueueUploads"/>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-3">
          <div class="lg:col-span-2 space-y-3">
            <FileExplorer :q="q" @select="select" @delete="onDelete"/>
            <UploadManager :queue="queue"/>
          </div>
          <div class="space-y-3">
            <PreviewPanel :file="selected" @delete="onDelete(selected)"/>
            <MetadataPanel :file="selected" @saved="refreshSelected"/>
            <ClusteringGraph v-if="graph" :graph="graph"/>
            <button class="btn w-full" @click="recluster">Recompute Clusters</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue'
import TopBar from '@/components/TopBar.vue'
import FileExplorer from '@/components/FileExplorer.vue'
import PreviewPanel from '@/components/PreviewPanel.vue'
import MetadataPanel from '@/components/MetadataPanel.vue'
import UploadManager from '@/components/UploadManager.vue'
import ClusteringGraph from '@/components/ClusteringGraph.client.vue'

const { createFolder: apiCreateFolder, uploadFile, fileDetail, deleteFile, recluster, getClusters } = useApi()
const q = ref('')
const active = ref('files')
const selected = ref<any|null>(null)
const queue = ref<{ id:string, file:File, progress:number }[]>([])
const graph = ref<any>(null)

async function createFolder(){
  const name = prompt('Folder name?')
  if (!name) return
  await apiCreateFolder(name)
}

function enqueueUploads(files: File[]){
  for (const f of files){
    const id = crypto.randomUUID(); queue.value.push({ id, file: f, progress: 0 })
    uploadFile(f).then(() => {
      const idx = queue.value.findIndex(x=>x.id===id)
      if (idx>=0){ queue.value[idx].progress = 100; setTimeout(()=>queue.value.splice(idx,1), 500) }
    })
  }
}

async function select(f:any){ selected.value = await fileDetail(f.id) }
async function refreshSelected(){ if (selected.value) selected.value = await fileDetail(selected.value.id) }
async function onDelete(f:any){ if (!f) return; if (confirm('Delete file?')){ await deleteFile(f.id); selected.value=null } }

async function loadGraph(){ graph.value = await getClusters() }
async function doRecluster(){ graph.value = await recluster() }
const recluster = doRecluster

onMounted(loadGraph)
</script>
