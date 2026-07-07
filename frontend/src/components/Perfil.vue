<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()

const usuarioLogado = ref(null)
const usuario = ref(null)
const reviews = ref([])
const loading = ref(false)
const salvando = ref(false)
const removendo = ref(false)
const mensagem = ref('')
const erro = ref('')
const avatarFile = ref(null)
const avatarPreview = ref('')
const previewObjectUrl = ref('')

const isHeaderMinimized = ref(false)
const perfilMinimized = ref(false)
const editarMinimized = ref(false)
const resumoMinimized = ref(false)
const historicoMinimized = ref(false)

const form = ref({
  user_username: '',
  user_bio: '',
  user_password: '',
})

const baseUrl = computed(() => (apiBase || '').replace(/\/api\/?$/, ''))
const perfilIdRota = computed(() => {
  const id = Number(route.params.id)
  return Number.isFinite(id) && id > 0 ? id : null
})

const carregarUsuarioLogado = () => {
  const savedUser = localStorage.getItem('albumDaSemanaUser')
  usuarioLogado.value = savedUser ? JSON.parse(savedUser) : null
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

const sincronizarUsuario = (dados) => {
  const storageUser = {
    id: dados.id,
    user_username: dados.user_username,
    user_email: dados.user_email,
    user_bio: dados.user_bio || '',
    user_avatar: dados.user_avatar || '',
    is_admin: dados.is_admin,
  }

  localStorage.setItem('albumDaSemanaUser', JSON.stringify(storageUser))
  window.dispatchEvent(new Event('album-user-changed'))
  usuarioLogado.value = storageUser
}

const limparPreviewLocal = () => {
  if (previewObjectUrl.value) {
    URL.revokeObjectURL(previewObjectUrl.value)
    previewObjectUrl.value = ''
  }
}

const carregarPerfil = async () => {
  carregarUsuarioLogado()

  const alvoId = perfilIdRota.value || usuarioLogado.value?.id

  if (!alvoId) {
    router.push('/login')
    return
  }

  loading.value = true
  erro.value = ''

  try {
    const response = await fetch(`${apiBase}/users/${alvoId}/perfil/`)
    if (!response.ok) {
      throw new Error('Falha ao carregar perfil')
    }

    const data = await response.json()

    if (usuarioLogado.value?.id === data.id) {
      sincronizarUsuario(data)
    }

    usuario.value = {
      id: data.id,
      user_username: data.user_username,
      user_email: data.user_email,
      user_bio: data.user_bio || '',
      user_avatar: data.user_avatar || '',
      is_admin: data.is_admin,
    }
    reviews.value = data.reviews || []
    form.value = {
      user_username: data.user_username || '',
      user_bio: data.user_bio || '',
      user_password: '',
    }
    avatarPreview.value = normalizarAvatar(data.user_avatar)
  } catch (error) {
    erro.value = 'Não foi possível carregar os dados do perfil.'
    usuario.value = null
    reviews.value = []
  } finally {
    loading.value = false
  }
}

const selecionarAvatar = (event) => {
  const [file] = event.target.files || []
  avatarFile.value = file || null
  limparPreviewLocal()

  if (avatarFile.value) {
    previewObjectUrl.value = URL.createObjectURL(avatarFile.value)
    avatarPreview.value = previewObjectUrl.value
  } else {
    avatarPreview.value = normalizarAvatar(usuario.value?.user_avatar)
  }
}

const salvarPerfil = async () => {
  if (!perfilProprio.value || !usuarioLogado.value?.id) return

  salvando.value = true
  erro.value = ''
  mensagem.value = ''

  try {
    const payload = new FormData()
    payload.append('id', usuarioLogado.value.id)
    payload.append('user_username', form.value.user_username.trim())
    payload.append('user_bio', form.value.user_bio || '')

    if (form.value.user_password.trim()) {
      payload.append('user_password', form.value.user_password.trim())
    }

    if (avatarFile.value) {
      payload.append('user_avatar', avatarFile.value)
    }

    const response = await fetch(`${apiBase}/users/${usuarioLogado.value.id}/perfil/`, {
      method: 'PUT',
      body: payload,
    })

    if (!response.ok) {
      throw new Error('Falha ao salvar perfil')
    }

    const data = await response.json()
    sincronizarUsuario(data)
    usuario.value = {
      id: data.id,
      user_username: data.user_username,
      user_email: data.user_email,
      user_bio: data.user_bio || '',
      user_avatar: data.user_avatar || '',
      is_admin: data.is_admin,
    }
    reviews.value = data.reviews || reviews.value
    form.value.user_password = ''
    avatarFile.value = null
    limparPreviewLocal()
    mensagem.value = 'Perfil atualizado com sucesso.'
  } catch (error) {
    erro.value = 'Não foi possível atualizar o perfil.'
  } finally {
    salvando.value = false
  }
}

const deletarConta = async () => {
  if (!perfilProprio.value || !usuarioLogado.value?.id) return

  const confirmar = window.confirm('Tem certeza que deseja deletar sua conta? Esta ação não pode ser desfeita.')
  if (!confirmar) return

  removendo.value = true
  erro.value = ''

  try {
    const response = await fetch(`${apiBase}/users/${usuarioLogado.value.id}/perfil/`, {
      method: 'DELETE',
    })

    if (!response.ok && response.status !== 204) {
      throw new Error('Falha ao deletar conta')
    }

    localStorage.removeItem('albumDaSemanaUser')
    window.dispatchEvent(new Event('album-user-changed'))
    router.push('/login')
  } catch (error) {
    erro.value = 'Não foi possível deletar sua conta.'
  } finally {
    removendo.value = false
  }
}

const sair = () => {
  localStorage.removeItem('albumDaSemanaUser')
  window.dispatchEvent(new Event('album-user-changed'))
  usuarioLogado.value = null
  router.push('/login')
}

const formatoData = (valor) => {
  return new Date(valor).toLocaleDateString('pt-BR')
}

const temUsuario = computed(() => Boolean(usuario.value))
const perfilProprio = computed(() => {
  if (!usuario.value?.id || !usuarioLogado.value?.id) return false
  return usuario.value.id === usuarioLogado.value.id
})
const tituloPerfil = computed(() => {
  if (!temUsuario.value) return 'Perfil'
  return perfilProprio.value ? 'Meu Perfil' : `Perfil de ${usuario.value.user_username}`
})
const avatarExibido = computed(() => {
  if (!usuario.value) return ''
  if (previewObjectUrl.value) {
    return previewObjectUrl.value
  }

  return normalizarAvatar(usuario.value?.user_avatar || avatarPreview.value)
})

onMounted(() => {
  carregarPerfil()
})

watch(() => route.params.id, () => {
  carregarPerfil()
})

onBeforeUnmount(() => {
  limparPreviewLocal()
})
</script>

<template>
  <div class="perfil-page">
    <div v-if="isHeaderMinimized" class="window minimized-bar">
      <div class="title-bar">
        <div class="title-bar-text">AlbumDaSemana minimizado</div>
      </div>
      <div class="window-body minimized-body">
        <button type="button" @click="isHeaderMinimized = false">Restaurar</button>
      </div>
    </div>
    <HomeHeader v-else @minimize="isHeaderMinimized = true" />

    <div class="window perfil-window">
      <div class="title-bar">
        <div class="title-bar-text">{{ tituloPerfil }}</div>
        <div class="title-bar-controls">
          <button type="button" aria-label="Minimize" @click="perfilMinimized = !perfilMinimized"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close"></button>
        </div>
      </div>

      <div class="window-body" v-show="!perfilMinimized">
        <div v-if="temUsuario" class="perfil-conteudo">
          <div v-if="loading" class="estado">Carregando perfil...</div>

          <template v-else>
            <div class="perfil-header">
              <div class="avatar-wrap">
                <img v-if="avatarExibido" :src="avatarExibido" :alt="usuario.user_username" class="avatar" />
                <div v-else class="avatar placeholder">{{ usuario.user_username?.charAt(0)?.toUpperCase() }}</div>
              </div>
              <div class="perfil-identidade">
                <h2>{{ usuario.user_username }}</h2>
                <p v-if="perfilProprio">{{ usuario.user_email }}</p>
                <p v-if="usuario.user_bio" class="bio-text">{{ usuario.user_bio }}</p>
                <p v-else class="bio-text vazio">Sem bio cadastrada.</p>
              </div>
            </div>

            <div class="perfil-grid">
              <section v-if="perfilProprio" class="window bloco">
                <div class="title-bar">
                  <div class="title-bar-text">Editar perfil</div>
                  <div class="title-bar-controls">
                    <button type="button" aria-label="Minimize" @click="editarMinimized = !editarMinimized"></button>
                    <button aria-label="Maximize"></button>
                    <button aria-label="Close"></button>
                  </div>
                </div>
                <div class="window-body" v-show="!editarMinimized">
                  <div class="field-row-stacked">
                    <label>E-mail</label>
                    <input :value="usuario.user_email" readonly />
                  </div>

                  <div class="field-row-stacked">
                    <label for="username">Nome</label>
                    <input id="username" v-model="form.user_username" type="text" />
                  </div>

                  <div class="field-row-stacked">
                    <label for="bio">Bio</label>
                    <textarea id="bio" v-model="form.user_bio" rows="4"></textarea>
                  </div>

                  <div class="field-row-stacked">
                    <label for="avatar">Avatar / foto de perfil</label>
                    <input id="avatar" type="file" accept="image/*" @change="selecionarAvatar" />
                    <small>Opcional. Selecione uma imagem para atualizar a foto do perfil.</small>
                  </div>

                  <div class="field-row-stacked">
                    <label for="password">Nova senha</label>
                    <input id="password" v-model="form.user_password" type="password" placeholder="Deixe em branco para manter a senha" />
                  </div>

                  <div class="actions">
                    <button type="button" :disabled="salvando" @click="salvarPerfil">
                      {{ salvando ? 'Salvando...' : 'Salvar alterações' }}
                    </button>
                  </div>
                </div>
              </section>

              <section class="window bloco">
                <div class="title-bar">
                  <div class="title-bar-text">Resumo</div>
                  <div class="title-bar-controls">
                    <button type="button" aria-label="Minimize" @click="resumoMinimized = !resumoMinimized"></button>
                    <button aria-label="Maximize"></button>
                    <button aria-label="Close"></button>
                  </div>
                </div>
                <div class="window-body resumo" v-show="!resumoMinimized">
                  <div>
                    <span class="resumo-label">Username</span>
                    <strong>{{ usuario.user_username }}</strong>
                  </div>
                  <div v-if="perfilProprio">
                    <span class="resumo-label">E-mail</span>
                    <strong>{{ usuario.user_email }}</strong>
                  </div>
                  <div>
                    <span class="resumo-label">Reviews feitas</span>
                    <strong>{{ reviews.length }}</strong>
                  </div>
                  <div>
                    <span class="resumo-label">ID</span>
                    <strong>{{ usuario.id }}</strong>
                  </div>
                </div>
              </section>
            </div>

            <section class="window bloco bloco-largo">
              <div class="title-bar">
                <div class="title-bar-text">Histórico de avaliações</div>
                <div class="title-bar-controls">
                  <button type="button" aria-label="Minimize" @click="historicoMinimized = !historicoMinimized"></button>
                  <button aria-label="Maximize"></button>
                  <button aria-label="Close"></button>
                </div>
              </div>
              <div class="window-body" v-show="!historicoMinimized">
                <div v-if="reviews.length" class="reviews-lista">
                  <article v-for="review in reviews" :key="review.id" class="review-card">
                    <div class="review-topo">
                      <div>
                        <strong>{{ review.alvo_titulo }}</strong>
                        <span v-if="review.alvo_artista"> - {{ review.alvo_artista }}</span>
                      </div>
                      <span>{{ formatoData(review.criado_em) }}</span>
                    </div>
                    <p class="review-tipo">{{ review.alvo_tipo === 'album' ? 'Álbum' : 'Música' }}</p>
                    <p v-if="review.nota" class="review-estrelas">
                      <span v-for="n in 5" :key="n" :class="{ preenchida: n <= review.nota }">★</span>
                      <span class="review-nota">{{ review.nota }}/5</span>
                    </p>
                    <p class="review-texto">{{ review.texto }}</p>
                    <div class="review-metrica">Likes {{ review.likes }} | Deslikes {{ review.dislikes }}</div>
                  </article>
                </div>
                <div v-else class="estado">{{ perfilProprio ? 'Você ainda não publicou reviews.' : 'Este usuário ainda não publicou reviews.' }}</div>
              </div>
            </section>

            <div v-if="perfilProprio && mensagem" class="status sucesso">{{ mensagem }}</div>
            <div v-if="erro" class="status erro">{{ erro }}</div>

            <div v-if="perfilProprio" class="acoes-finais">
              <button type="button" class="perigo" :disabled="removendo" @click="deletarConta">
                {{ removendo ? 'Removendo...' : 'Deletar conta' }}
              </button>
              <button type="button" @click="sair">Sair</button>
            </div>
          </template>
        </div>

        <div v-else class="sem-sessao">
          <p>Nenhum perfil encontrado.</p>
          <button type="button" @click="router.push('/login')">Ir para login</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.perfil-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  min-height: 100vh;
  padding: 10px;
  box-sizing: border-box;
}

.perfil-window {
  width: 100%;
  max-width: 980px;
  margin: 10px auto;
}

.minimized-bar {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.minimized-body {
  display: flex;
  justify-content: center;
  padding: 12px;
}

.perfil-conteudo {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.perfil-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 4px;
}

.avatar-wrap {
  flex: 0 0 auto;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: bold;
  background: #d6d6d6;
}

.placeholder {
  color: #000;
}

.perfil-identidade h2 {
  margin: 0;
}

.perfil-identidade p {
  margin: 4px 0 0;
}

.bio-text {
  max-width: 720px;
}

.bio-text.vazio {
  color: #666;
}

.perfil-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.bloco,
.bloco-largo {
  width: 100%;
}

.resumo {
  display: grid;
  gap: 12px;
}

.resumo-label {
  display: block;
  font-size: 12px;
  color: #666;
}

.reviews-lista {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.review-card {
  border: 1px solid #bdbdbd;
  padding: 10px;
  background: #fff;
}

.review-topo {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 13px;
}

.review-tipo,
.review-metrica {
  margin: 6px 0 0;
  color: #666;
  font-size: 12px;
}

.review-estrelas {
  margin: 6px 0 0;
  color: #bbb;
  font-size: 14px;
  letter-spacing: 1px;
}

.review-estrelas .preenchida {
  color: #d4a017;
}

.review-nota {
  margin-left: 8px;
  color: #666;
  font-size: 12px;
}

.review-texto {
  white-space: pre-wrap;
  margin: 8px 0 0;
}

.field-row-stacked {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
}

.acoes-finais {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  flex-wrap: wrap;
}

.status {
  padding: 8px 10px;
  border: 1px solid #000;
}

.status.sucesso {
  background: #e9f7e9;
}

.status.erro {
  background: #ffe8e8;
}

.estado {
  color: #666;
}

.perigo {
  color: #7a0000;
}

.sem-sessao {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

@media (max-width: 800px) {
  .perfil-grid {
    grid-template-columns: 1fr;
  }

  .perfil-header {
    align-items: flex-start;
  }
}
</style>