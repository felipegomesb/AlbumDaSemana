<script setup>
import { ref, onMounted } from 'vue'
import ReviewSection from './ReviewSection.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const musica = ref(null)
const loading = ref(true)
const erro = ref('')

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const carregarMusica = async () => {
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
}

const reagir = async (action) => {
  if (!musica.value) return

  try {
    const response = await fetch(`${apiBase}/musicas/${musica.value.id}/react/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    })

    if (!response.ok) throw new Error('Falha ao reagir')

    musica.value = await response.json()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  carregarMusica()
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
          <p class="contadores">Posts: {{ musica.review_count || 0 }} | Likes: {{ musica.likes || 0 }} | Deslikes: {{ musica.dislikes || 0 }}</p>
          <div class="reacoes">
            <button type="button" @click="reagir('like')">Like</button>
            <button type="button" @click="reagir('dislike')">Deslike</button>
          </div>
        </div>
      </div>

      <ReviewSection
        v-if="musica"
        target-type="musica"
        :target-id="musica.id"
        titulo="Música"
        @changed="carregarMusica"
      />
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

.contadores {
  margin-top: 6px;
  color: #333;
  font-size: 13px;
}

.loading, .erro {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>
