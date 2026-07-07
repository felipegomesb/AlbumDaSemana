<script setup>
import { ref, computed, onMounted } from 'vue'
import ReviewSection from './ReviewSection.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const musica = ref(null)
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

const carregarMusica = async () => {
  try {
    const saved = localStorage.getItem('albumDaSemanaUser')
    usuario.value = saved ? JSON.parse(saved) : null
    const uid = usuario.value?.id || ''
    const response = await fetch(`${apiBase}/musica-do-dia/?usuario_id=${uid}`)
    if (!response.ok) throw new Error('Sem música do dia')
    const data = await response.json()
    musica.value = data.musica
    userReaction.value = data.user_reaction || null
  } catch (e) {
    erro.value = 'Nenhuma música cadastrada ainda.'
  } finally {
    loading.value = false
  }
}

const isAdmin = computed(() => usuario.value?.is_admin === true)

const removerMusicaDoDia = async () => {
  if (!window.confirm('Tem certeza que deseja remover a Musica do Dia?')) return
  try {
    const response = await fetch(`${apiBase}/musica-do-dia/definir/`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuario_id: usuario.value.id })
    })
    if (response.status === 204 || response.ok) {
      musica.value = null
      erro.value = 'Musica do dia removida. Uma nova sera sorteada automaticamente.'
    }
  } catch (e) {
    console.error(e)
  }
}

const reagir = async (action) => {
  if (!musica.value || !usuario.value) return

  try {
    const response = await fetch(`${apiBase}/musicas/${musica.value.id}/react/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, usuario_id: usuario.value.id })
    })

    if (!response.ok) throw new Error('Falha ao reagir')

    const data = await response.json()
    musica.value = data
    userReaction.value = data.user_reaction
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
        <button type="button" aria-label="Minimize" @click="isMinimized = !isMinimized"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body" v-show="!isMinimized">
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
          <p v-if="musica.nota_media" class="nota-media">
            <span class="estrelas-exibicao">
              <span v-for="n in 5" :key="n" :class="{ preenchida: n <= Math.round(musica.nota_media) }">★</span>
            </span>
            <span class="nota-valor">{{ musica.nota_media }}/5</span>
          </p>
          <p>Artista: {{ musica.artista }}</p>
          <p v-if="musica.album_nome">Álbum: {{ musica.album_nome }}</p>
          <p v-if="musica.genero">Gênero: {{ musica.genero }}</p>
          <p v-if="musica.duracao_ms">Duração: {{ formatarDuracao(musica.duracao_ms) }}</p>
          <p class="contadores">Posts: {{ musica.review_count || 0 }}</p>
          <div v-if="usuario" class="reacoes">
            <button type="button" :class="{ ativo: userReaction === 'like' }" @click="reagir('like')">Like {{ musica.likes || 0 }}</button>
            <button type="button" :class="{ ativo: userReaction === 'dislike' }" @click="reagir('dislike')">Deslike {{ musica.dislikes || 0 }}</button>
          </div>
          <div v-if="isAdmin" class="admin-actions">
            <button type="button" class="btn-remover" @click="removerMusicaDoDia">Remover Musica do Dia</button>
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

.reacoes {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

.reacoes button.ativo {
  font-weight: bold;
  box-shadow: inset 1px 1px 2px #000;
}

.admin-actions {
  margin-top: 8px;
  display: flex;
  gap: 6px;
}

.btn-remover {
  color: #7a0000;
}

.loading, .erro {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>