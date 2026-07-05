<script setup>
import { ref, onMounted } from 'vue'
import ReviewSection from './ReviewSection.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const album = ref(null)
const userReaction = ref(null)
const usuario = ref(null)
const loading = ref(true)
const erro = ref('')
const isMinimized = ref(false)

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const carregarAlbum = async () => {
  try {
    const saved = localStorage.getItem('albumDaSemanaUser')
    usuario.value = saved ? JSON.parse(saved) : null
    const uid = usuario.value?.id || ''
    const response = await fetch(`${apiBase}/album-da-semana/?usuario_id=${uid}`)
    if (!response.ok) throw new Error('Sem álbum da semana')
    const data = await response.json()
    album.value = data.album
    userReaction.value = data.user_reaction || null
  } catch (e) {
    erro.value = 'Nenhum álbum cadastrado ainda.'
  } finally {
    loading.value = false
  }
}

const reagir = async (action) => {
  if (!album.value || !usuario.value) return

  try {
    const response = await fetch(`${apiBase}/albuns/${album.value.id}/react/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, usuario_id: usuario.value.id })
    })

    if (!response.ok) throw new Error('Falha ao reagir')

    const data = await response.json()
    album.value = data
    userReaction.value = data.user_reaction
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  carregarAlbum()
})
</script>

<template>
  <div class="window album-card">
    <div class="title-bar">
      <div class="title-bar-text">Álbum da Semana</div>
      <div class="title-bar-controls">
        <button type="button" aria-label="Minimize" @click="isMinimized = !isMinimized"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body" v-show="!isMinimized">
      <div v-if="loading" class="loading">Carregando...</div>

      <div v-else-if="erro" class="erro">{{ erro }}</div>

      <div v-else-if="album" class="album-content">
        <img
          v-if="album.capa_url"
          :src="album.capa_url"
          :alt="album.titulo"
          class="capa"
        />
        <div class="info">
          <p class="titulo"><strong>{{ album.titulo }}</strong></p>
          <p v-if="album.nota_media" class="nota-media">
            <span class="estrelas-exibicao">
              <span v-for="n in 5" :key="n" :class="{ preenchida: n <= Math.round(album.nota_media) }">★</span>
            </span>
            <span class="nota-valor">{{ album.nota_media }}/5</span>
          </p>
          <p>Artista: {{ album.artista }}</p>
          <p v-if="album.ano">Ano: {{ album.ano }}</p>
          <p v-if="album.genero">Gênero: {{ album.genero }}</p>
          <p class="contadores">Posts: {{ album.review_count || 0 }}</p>
          <div v-if="usuario" class="reacoes">
            <button type="button" :class="{ ativo: userReaction === 'like' }" @click="reagir('like')">Like {{ album.likes || 0 }}</button>
            <button type="button" :class="{ ativo: userReaction === 'dislike' }" @click="reagir('dislike')">Deslike {{ album.dislikes || 0 }}</button>
          </div>

          <div v-if="album.faixas && album.faixas.length" class="faixas-section">
            <details>
              <summary>Faixas ({{ album.faixas.length }})</summary>
              <ul class="tree-view">
                <li v-for="faixa in album.faixas" :key="faixa.id">
                  {{ faixa.numero }}. {{ faixa.titulo }}
                  <span class="duracao">{{ formatarDuracao(faixa.duracao_ms) }}</span>
                </li>
              </ul>
            </details>
          </div>
        </div>
      </div>

      <ReviewSection
        v-if="album"
        target-type="album"
        :target-id="album.id"
        titulo="Álbum"
        @changed="carregarAlbum"
      />
    </div>
  </div>
</template>

<style scoped>
.album-card {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.album-content {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.capa {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border: 2px solid #000;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.titulo {
  font-size: 20px;
}

.nota-media {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 2px 0;
}

.estrelas-exibicao {
  font-size: 15px;
  color: #bbb;
  letter-spacing: 1px;
}

.estrelas-exibicao span.preenchida {
  color: #d4a017;
}

.nota-valor {
  font-size: 12px;
  color: #666;
}

.contadores {
  margin-top: 6px;
  color: #333;
  font-size: 13px;
}

.faixas-section {
  margin-top: 8px;
}

.tree-view {
  list-style: none;
  padding-left: 16px;
  margin: 4px 0;
}

.tree-view li {
  padding: 2px 0;
  font-size: 13px;
}

.duracao {
  color: #666;
  margin-left: 8px;
}

.reacoes {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

.reacoes button.ativo {
  font-weight: bold;
  box-shadow: inset 1px 1px 2px #000;
}

.loading, .erro {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>