<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'
import ReviewSection from './ReviewSection.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()
const album = ref(null)
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

const carregarAlbum = async () => {
  loading.value = true
  erro.value = ''
  try {
    const uid = usuario.value?.id || ''
    const res = await fetch(`${apiBase}/albuns/${route.params.id}/?usuario_id=${uid}`)
    if (!res.ok) throw new Error()
    album.value = await res.json()
    userReaction.value = album.value.user_reaction || null
  } catch {
    erro.value = 'Não foi possível carregar o álbum.'
  } finally {
    loading.value = false
  }
}

const reagir = async (action) => {
  if (!usuario.value) return
  try {
    const res = await fetch(`${apiBase}/albuns/${route.params.id}/react/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, usuario_id: usuario.value.id }),
    })
    if (res.ok) {
      const data = await res.json()
      album.value.likes = data.likes
      album.value.dislikes = data.dislikes
      userReaction.value = data.user_reaction
    }
  } catch { /* silencioso */ }
}

onMounted(() => {
  carregarUsuario()
  carregarAlbum()
})
</script>

<template>
  <div class="detalhe-page">
    <HomeHeader />

    <div v-if="loading" class="window detalhe-window">
      <div class="title-bar">
        <div class="title-bar-text">Carregando...</div>
      </div>
      <div class="window-body estado">Carregando álbum...</div>
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
          <div class="title-bar-text">{{ album.titulo }} - {{ album.artista }}</div>
          <div class="title-bar-controls">
            <button aria-label="Minimize"></button>
            <button aria-label="Maximize"></button>
            <button aria-label="Close" @click="router.back()"></button>
          </div>
        </div>

        <div class="window-body detalhe-body">
          <div class="detalhe-info">
            <img v-if="album.capa_url" :src="album.capa_url" class="detalhe-capa" :alt="album.titulo" />
            <div class="detalhe-dados">
              <h2>{{ album.titulo }}</h2>
              <p><strong>Artista:</strong> {{ album.artista }}</p>
              <p v-if="album.ano"><strong>Ano:</strong> {{ album.ano }}</p>
              <p v-if="album.genero"><strong>Gênero:</strong> <span class="tag-genero">{{ album.genero }}</span></p>

              <div v-if="usuario" class="reacoes">
                <button :class="{ ativo: userReaction === 'like' }" @click="reagir('like')">
                  Like {{ album.likes || 0 }}
                </button>
                <button :class="{ ativo: userReaction === 'dislike' }" @click="reagir('dislike')">
                  Dislike {{ album.dislikes || 0 }}
                </button>
              </div>
            </div>
          </div>

          <fieldset v-if="album.faixas && album.faixas.length" class="faixas-fieldset">
            <legend>Faixas ({{ album.faixas.length }})</legend>
            <ul class="tree-view">
              <li v-for="f in album.faixas" :key="f.id">
                {{ f.numero }}. {{ f.titulo }}
                <span class="faixa-duracao">{{ formatarDuracao(f.duracao_ms) }}</span>
              </li>
            </ul>
          </fieldset>
        </div>
      </div>

      <div class="review-container">
        <ReviewSection
          v-if="album.id"
          target-type="album"
          :target-id="album.id"
          :titulo="album.titulo"
          @changed="carregarAlbum"
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

.faixas-fieldset {
  margin-top: 16px;
}

.faixa-duracao {
  color: #808080;
  font-size: 12px;
  margin-left: 8px;
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
