<script setup>
import { ref, onMounted } from 'vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const musicasAnteriores = ref([])
const albunsAnteriores = ref([])

const formatarData = (dataStr) => {
  const d = new Date(dataStr + 'T00:00:00')
  return d.toLocaleDateString('pt-BR')
}

onMounted(async () => {
  try {
    const [musicasRes, albunsRes] = await Promise.all([
      fetch(`${apiBase}/historico/musicas/`),
      fetch(`${apiBase}/historico/albuns/`)
    ])

    if (musicasRes.ok) {
      const data = await musicasRes.json()
      musicasAnteriores.value = data.slice(1)
    }
    if (albunsRes.ok) {
      const data = await albunsRes.json()
      albunsAnteriores.value = data.slice(1)
    }
  } catch (e) {
    console.error('Erro ao carregar histórico:', e)
  }
})
</script>

<template>
  <div v-if="musicasAnteriores.length || albunsAnteriores.length" class="historico-container">

    <div v-if="musicasAnteriores.length" class="window historico-window">
      <div class="title-bar">
        <div class="title-bar-text">Músicas Anteriores</div>
        <div class="title-bar-controls">
          <button aria-label="Minimize"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close"></button>
        </div>
      </div>
      <div class="window-body">
        <table class="historico-table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Música</th>
              <th>Artista</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entrada in musicasAnteriores" :key="entrada.id">
              <td>{{ formatarData(entrada.data) }}</td>
              <td>{{ entrada.musica.titulo }}</td>
              <td>{{ entrada.musica.artista }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="albunsAnteriores.length" class="window historico-window">
      <div class="title-bar">
        <div class="title-bar-text">Álbuns Anteriores</div>
        <div class="title-bar-controls">
          <button aria-label="Minimize"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close"></button>
        </div>
      </div>
      <div class="window-body">
        <div class="albuns-grid">
          <div v-for="entrada in albunsAnteriores" :key="entrada.id" class="album-mini">
            <img
              v-if="entrada.album.capa_url"
              :src="entrada.album.capa_url"
              :alt="entrada.album.titulo"
              class="mini-capa"
            />
            <div class="mini-info">
              <strong>{{ entrada.album.titulo }}</strong>
              <span>{{ entrada.album.artista }}</span>
              <span class="mini-data">Semana de {{ formatarData(entrada.semana_inicio) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.historico-container {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.historico-window {
  width: 100%;
}

.historico-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.historico-table th,
.historico-table td {
  text-align: left;
  padding: 4px 8px;
  border-bottom: 1px solid #ccc;
}

.albuns-grid {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.album-mini {
  display: flex;
  gap: 8px;
  align-items: center;
  flex: 1 1 calc(50% - 12px);
  min-width: 200px;
}

.mini-capa {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border: 1px solid #000;
}

.mini-info {
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.mini-data {
  color: #666;
}
</style>
