<script setup>
import { ref, onMounted } from 'vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const musica = ref(null)
const loading = ref(true)
const erro = ref('')

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

onMounted(async () => {
  try {
    const response = await fetch(`${apiBase}/musica-do-dia/`)
    if (!response.ok) throw new Error('Sem música do dia')
    const data = await response.json()
    musica.value = data.musica
  } catch (e) {
    erro.value = 'Nenhuma música cadastrada ainda.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="window musica-card">
    <div class="title-bar">
      <div class="title-bar-text">Música do Dia</div>
      <div class="title-bar-controls">
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body">
      <div v-if="loading" class="loading">Carregando...</div>

      <div v-else-if="erro" class="erro">{{ erro }}</div>

      <div v-else-if="musica" class="musica-content">
        <img
          v-if="musica.capa_url"
          :src="musica.capa_url"
          :alt="musica.titulo"
          class="capa"
        />
        <div class="info">
          <p class="titulo"><strong>{{ musica.titulo }}</strong></p>
          <p>Artista: {{ musica.artista }}</p>
          <p v-if="musica.album_nome">Álbum: {{ musica.album_nome }}</p>
          <p v-if="musica.genero">Gênero: {{ musica.genero }}</p>
          <p v-if="musica.duracao_ms">Duração: {{ formatarDuracao(musica.duracao_ms) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.musica-card {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.musica-content {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.capa {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border: 2px solid #000;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.titulo {
  font-size: 18px;
}

.loading, .erro {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>
