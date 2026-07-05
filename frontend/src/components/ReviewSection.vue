<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const props = defineProps({
  targetType: {
    type: String,
    required: true,
  },
  targetId: {
    type: Number,
    required: true,
  },
  titulo: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['changed'])

const apiBase = import.meta.env.VITE_API_BASE_URL
const baseUrl = computed(() => (apiBase || '').replace(/\/api\/?$/, ''))
const usuario = ref(null)
const reviews = ref([])
const loading = ref(false)
const enviando = ref(false)
const mensagem = ref('')
const novoTexto = ref('')
const notaSelecionada = ref(0)
const notaHover = ref(0)
const isMinimized = ref(false)

const endpoint = computed(() => {
  const tipo = props.targetType === 'album' ? 'albuns' : 'musicas'
  return `${apiBase}/reviews/${tipo}/${props.targetId}/`
})

const reviewDoUsuario = computed(() => {
  if (!usuario.value) return null
  return reviews.value.find((r) => r.usuario === usuario.value.id) || null
})

const carregarUsuario = () => {
  const savedUser = localStorage.getItem('albumDaSemanaUser')
  usuario.value = savedUser ? JSON.parse(savedUser) : null
}

const normalizarAvatar = (valor) => {
  if (!valor) return ''
  if (valor.startsWith('http://') || valor.startsWith('https://') || valor.startsWith('blob:')) {
    return valor
  }
  if (valor.startsWith('/')) {
    return `${baseUrl.value}${valor}`
  }
  return `${baseUrl.value}/${valor}`
}

const carregarReviews = async (preencherForm = false) => {
  loading.value = true
  mensagem.value = ''

  try {
    const uid = usuario.value?.id || ''
    const response = await fetch(`${endpoint.value}?usuario_id=${uid}`)
    if (!response.ok) {
      throw new Error('Falha ao carregar reviews')
    }

    reviews.value = await response.json()

    if (preencherForm && reviewDoUsuario.value) {
      novoTexto.value = reviewDoUsuario.value.texto
      notaSelecionada.value = reviewDoUsuario.value.nota || 0
    }
  } catch (error) {
    mensagem.value = 'Não foi possível carregar as reviews.'
  } finally {
    loading.value = false
  }
}

const publicarReview = async () => {
  if (!usuario.value) {
    mensagem.value = 'Faça login para publicar uma review.'
    return
  }

  const texto = novoTexto.value.trim()
  if (!texto) return

  if (!notaSelecionada.value) {
    mensagem.value = 'Selecione uma nota de 1 a 5 estrelas.'
    return
  }

  enviando.value = true
  mensagem.value = ''

  try {
    const response = await fetch(endpoint.value, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        texto,
        nota: notaSelecionada.value,
        autor_nome: usuario.value.user_username,
        usuario_id: usuario.value.id,
      }),
    })

    if (!response.ok) {
      throw new Error('Falha ao publicar review')
    }

    await carregarReviews(true)
    emit('changed')
  } catch (error) {
    mensagem.value = 'Não foi possível publicar sua review.'
  } finally {
    enviando.value = false
  }
}

const reagir = async (reviewId, action) => {
  if (!usuario.value) {
    mensagem.value = 'Faça login para reagir.'
    return
  }

  try {
    const response = await fetch(`${apiBase}/reviews/${reviewId}/reaction/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, usuario_id: usuario.value.id }),
    })

    if (!response.ok) {
      throw new Error('Falha na reação')
    }

    await carregarReviews()
    emit('changed')
  } catch (error) {
    mensagem.value = 'Não foi possível registrar sua reação.'
  }
}

const formatarData = (dataStr) => {
  const data = new Date(dataStr)
  return data.toLocaleDateString('pt-BR')
}

onMounted(() => {
  carregarUsuario()
  carregarReviews(true)
})

watch(() => props.targetId, () => {
  carregarReviews(true)
})
</script>

<template>
  <div class="window review-window">
    <div class="title-bar">
      <div class="title-bar-text">Reviews de {{ titulo }}</div>
      <div class="title-bar-controls">
        <button type="button" aria-label="Minimize" @click="isMinimized = !isMinimized"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body" v-show="!isMinimized">
      <form class="review-form" @submit.prevent="publicarReview">
        <div class="estrelas-input">
          <span class="estrelas-label">Sua nota:</span>
          <button
            v-for="n in 5"
            :key="n"
            type="button"
            class="estrela-btn"
            :class="{ preenchida: n <= (notaHover || notaSelecionada) }"
            @click="notaSelecionada = n"
            @mouseenter="notaHover = n"
            @mouseleave="notaHover = 0"
          >★</button>
          <span v-if="notaSelecionada" class="estrelas-valor">{{ notaSelecionada }}/5</span>
        </div>
        <textarea
          v-model="novoTexto"
          class="review-textarea"
          rows="4"
          placeholder="Escreva sua review..."
        />
        <div class="review-actions">
          <span v-if="usuario && reviewDoUsuario" class="autor">Editando sua review de {{ usuario.user_username }}</span>
          <span v-else-if="usuario" class="autor">Publicando como {{ usuario.user_username }}</span>
          <span v-else class="autor alerta">Faça login para publicar</span>
          <button type="submit" :disabled="enviando || !usuario">
            {{ enviando ? 'Salvando...' : (reviewDoUsuario ? 'Atualizar review' : 'Publicar review') }}
          </button>
        </div>
      </form>

      <div v-if="mensagem" class="mensagem">{{ mensagem }}</div>

      <div v-if="loading" class="estado">Carregando reviews...</div>
      <div v-else-if="reviews.length" class="reviews-lista">
        <article v-for="review in reviews" :key="review.id" class="review-item">
          <div class="review-topo">
            <div class="review-autor">
              <img
                v-if="review.usuario_avatar"
                :src="normalizarAvatar(review.usuario_avatar)"
                :alt="review.usuario_username"
                class="avatar-quadrado"
              />
              <div v-else class="avatar-quadrado placeholder">
                {{ review.usuario_username?.charAt(0)?.toUpperCase() }}
              </div>
              <strong>{{ review.usuario_username }}</strong>
              <span v-if="review.nota" class="estrelas-exibicao">
                <span v-for="n in 5" :key="n" :class="{ preenchida: n <= review.nota }">★</span>
              </span>
            </div>
            <span>{{ formatarData(review.criado_em) }}</span>
          </div>
          <p class="review-texto">{{ review.texto }}</p>
          <div v-if="usuario" class="review-reacoes">
            <button type="button" :class="{ ativo: review.user_reaction === 'like' }" @click="reagir(review.id, 'like')">Like {{ review.likes }}</button>
            <button type="button" :class="{ ativo: review.user_reaction === 'dislike' }" @click="reagir(review.id, 'dislike')">Deslike {{ review.dislikes }}</button>
          </div>
        </article>
      </div>
      <div v-else class="estado">Ainda não existem reviews para este item.</div>
    </div>
  </div>
</template>

<style scoped>
.review-window {
  width: 100%;
  margin-top: 10px;
}

.review-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.estrelas-input {
  display: flex;
  align-items: center;
  gap: 2px;
}

.estrelas-label {
  font-size: 12px;
  margin-right: 6px;
}

.estrela-btn {
  border: 0;
  background: transparent;
  padding: 0 1px;
  font-size: 20px;
  line-height: 1;
  color: #bbb;
  cursor: pointer;
}

.estrela-btn.preenchida {
  color: #d4a017;
}

.estrelas-valor {
  margin-left: 6px;
  font-size: 12px;
  color: #666;
}

.estrelas-exibicao {
  font-size: 13px;
  color: #bbb;
  letter-spacing: 1px;
}

.estrelas-exibicao span.preenchida {
  color: #d4a017;
}

.review-textarea {
  width: 100%;
  resize: vertical;
}

.review-actions {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.autor {
  font-size: 12px;
}

.alerta {
  color: #8a5a00;
}

.mensagem,
.estado {
  margin-bottom: 10px;
  color: #666;
}

.reviews-lista {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.review-item {
  border: 1px solid #c0c0c0;
  padding: 8px;
  background: #fff;
}

.review-topo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #666;
}

.review-autor {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-quadrado {
  width: 28px;
  height: 28px;
  object-fit: cover;
  border: 1px solid #000;
  flex-shrink: 0;
}

.avatar-quadrado.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #d6d6d6;
  color: #000;
  font-size: 13px;
  font-weight: bold;
}

.review-texto {
  margin: 8px 0;
  white-space: pre-wrap;
}

.review-reacoes {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.review-reacoes button.ativo {
  font-weight: bold;
  box-shadow: inset 1px 1px 2px #000;
}
</style>