<template>
  <div ref="el" class="card p-3 h-80"></div>
</template>
<script setup lang="ts">
import { forceSimulation, forceManyBody, forceLink, forceCenter } from 'd3-force'
const props = defineProps<{ graph: { nodes: { id:number, label:string, cluster:number }[], edges: [number, number][] } }>()

const el = ref<HTMLElement|null>(null)
watch(() => props.graph, (g) => { if (g && el.value) render() }, { immediate: true })

function render() {
  const container = el.value!; container.innerHTML = ''
  const w = container.clientWidth, h = container.clientHeight
  const svgNS = 'http://www.w3.org/2000/svg'
  const svg = document.createElementNS(svgNS,'svg'); svg.setAttribute('width', String(w)); svg.setAttribute('height', String(h)); container.appendChild(svg)

  const nodes = props.graph.nodes.map(n => ({...n, x: Math.random()*w, y: Math.random()*h}))
  const links = props.graph.edges.map(e => ({ source: nodes.find(n=>n.id===e[0])!, target: nodes.find(n=>n.id===e[1])! }))

  const sim = forceSimulation(nodes).force('charge', forceManyBody()).force('link', forceLink(links).distance(60)).force('center', forceCenter(w/2,h/2))
  const g = document.createElementNS(svgNS,'g'); svg.appendChild(g)

  const lines = links.map(l => { const line = document.createElementNS(svgNS,'line'); line.setAttribute('stroke','rgba(255,255,255,0.2)'); g.appendChild(line); return { el: line, l } })
  const circles = nodes.map(n => { const c = document.createElementNS(svgNS,'circle'); c.setAttribute('r','6'); c.setAttribute('fill','white'); c.setAttribute('opacity', String(0.5 + (n.cluster%5)*0.1)); g.appendChild(c); return { el:c, n } })

  sim.on('tick', () => {
    lines.forEach(({el,l}) => { el.setAttribute('x1', String(l.source.x)); el.setAttribute('y1', String(l.source.y)); el.setAttribute('x2', String(l.target.x)); el.setAttribute('y2', String(l.target.y)) })
    circles.forEach(({el,n}) => { el.setAttribute('cx', String(n.x)); el.setAttribute('cy', String(n.y)) })
  })
}
</script>
