<script setup>
import { ref, onMounted } from 'vue'
import ReviewSection from './ReviewSection.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const album = ref(null)
const loading = ref(true)
const erro = ref('')

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const carregarAlbum = async () => {
  try {
    const response = await fetch(`${apiBase}/album-da-semana/`)
    if (!response.ok) throw new Error('Sem álbum da semana')
    const data = await response.json()
    album.value = data.album
  } catch (e) {
    erro.value = 'Nenhum álbum cadastrado ainda.'
  } finally {
    loading.value = false
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
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body">
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
          <p>Artista: {{ album.artista }}</p>
          <p v-if="album.ano">Ano: {{ album.ano }}</p>
          <p v-if="album.genero">Gênero: {{ album.genero }}</p>
          <p class="contadores">Posts: {{ album.review_count || 0 }} | Likes: {{ album.review_likes || 0 }} | Deslikes: {{ album.review_dislikes || 0 }}</p>

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

.loading, .erro {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>
