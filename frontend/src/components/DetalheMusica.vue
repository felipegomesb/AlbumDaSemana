<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'
import ReviewSection from './ReviewSection.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()
const musica = ref(null)
const loading = ref(true)
const erro = ref('')
const usuario = ref(null)
const userReaction = ref(null)

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const carregarUsuario = () => {
  const saved = localStorage.getItem('albumDaSemanaUser')
  usuario.value = saved ? JSON.parse(saved) : null
}

const carregarMusica = async () => {
  loading.value = true
  erro.value = ''
  try {
    const uid = usuario.value?.id || ''
    const res = await fetch(`${apiBase}/musicas/${route.params.id}/?usuario_id=${uid}`)
    if (!res.ok) throw new Error()
    musica.value = await res.json()
    userReaction.value = musica.value.user_reaction || null
  } catch {
    erro.value = 'Não foi possível carregar a música.'
  } finally {
    loading.value = false
  }
}

const reagir = async (action) => {
  if (!usuario.value) return
  try {
    const res = await fetch(`${apiBase}/musicas/${route.params.id}/react/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, usuario_id: usuario.value.id }),
    })
    if (res.ok) {
      const data = await res.json()
      musica.value.likes = data.likes
      musica.value.dislikes = data.dislikes
      userReaction.value = data.user_reaction
    }
  } catch { /* silencioso */ }
}

onMounted(() => {
  carregarUsuario()
  carregarMusica()
})
</script>

<template>
  <div class="detalhe-page">
    <HomeHeader />

    <div v-if="loading" class="window detalhe-window">
      <div class="title-bar">
        <div class="title-bar-text">Carregando...</div>
      </div>
      <div class="window-body estado">Carregando música...</div>
    </div>

    <div v-else-if="erro" class="window detalhe-window">
      <div class="title-bar">
        <div class="title-bar-text">Erro</div>
      </div>
      <div class="window-body estado">{{ erro }}</div>
    </div>

    <template v-else>
      <div class="window detalhe-window">
        <div class="title-bar">
          <div class="title-bar-text">{{ musica.titulo }} - {{ musica.artista }}</div>
          <div class="title-bar-controls">
            <button aria-label="Minimize"></button>
            <button aria-label="Maximize"></button>
            <button aria-label="Close" @click="router.back()"></button>
          </div>
        </div>

        <div class="window-body detalhe-body">
          <div class="detalhe-info">
            <img v-if="musica.capa_url" :src="musica.capa_url" class="detalhe-capa" :alt="musica.titulo" />
            <div class="detalhe-dados">
              <h2>{{ musica.titulo }}</h2>
              <p><strong>Artista:</strong> {{ musica.artista }}</p>
              <p v-if="musica.album_nome"><strong>Álbum:</strong> {{ musica.album_nome }}</p>
              <p v-if="musica.genero"><strong>Gênero:</strong> <span class="tag-genero">{{ musica.genero }}</span></p>
              <p v-if="musica.duracao_ms"><strong>Duração:</strong> {{ formatarDuracao(musica.duracao_ms) }}</p>

              <div v-if="usuario" class="reacoes">
                <button :class="{ ativo: userReaction === 'like' }" @click="reagir('like')">
                  Like {{ musica.likes || 0 }}
                </button>
                <button :class="{ ativo: userReaction === 'dislike' }" @click="reagir('dislike')">
                  Dislike {{ musica.dislikes || 0 }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="review-container">
        <ReviewSection
          v-if="musica.id"
          target-type="musica"
          :target-id="musica.id"
          :titulo="musica.titulo"
          @changed="carregarMusica"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
.detalhe-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-self: flex-start;
  width: 100%;
  padding: 10px;
  min-height: 100vh;
  box-sizing: border-box;
}

.detalhe-window {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.detalhe-body {
  padding: 12px;
}

.detalhe-info {
  display: flex;
  gap: 16px;
}

.detalhe-capa {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border: 2px solid #808080;
  flex-shrink: 0;
}

.detalhe-dados {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detalhe-dados h2 {
  margin: 0 0 8px;
  font-size: 18px;
}

.detalhe-dados p {
  margin: 2px 0;
  font-size: 13px;
}

.tag-genero {
  background: #c0c0c0;
  border: 1px solid #808080;
  padding: 1px 6px;
  font-size: 11px;
}

.reacoes {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.reacoes button.ativo {
  font-weight: bold;
  box-shadow: inset 1px 1px 2px #000;
}

.review-container {
  width: 100%;
  max-width: 900px;
}

.estado {
  text-align: center;
  padding: 20px;
  color: #666;
}

@media (max-width: 500px) {
  .detalhe-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>
