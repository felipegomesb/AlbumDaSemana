<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const router = useRouter()

const usuario = ref(null)
const searchQuery = ref('')
const searchType = ref('track')
const resultados = ref([])
const loading = ref(false)
const mensagem = ref('')

onMounted(() => {
  const saved = localStorage.getItem('albumDaSemanaUser')
  usuario.value = saved ? JSON.parse(saved) : null
  if (!usuario.value?.is_admin) {
    router.push('/')
  }
})

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const buscarSpotify = async () => {
  if (!searchQuery.value.trim()) return
  loading.value = true
  mensagem.value = ''
  resultados.value = []

  try {
    const response = await fetch(
      `${apiBase}/spotify/search/?q=${encodeURIComponent(searchQuery.value)}&type=${searchType.value}&usuario_id=${usuario.value.id}`
    )
    if (!response.ok) {
      mensagem.value = 'Erro ao buscar no Spotify. Verifique as credenciais.'
      return
    }

    const data = await response.json()

    if (searchType.value === 'track' && data.tracks) {
      resultados.value = data.tracks.items.map(track => ({
        tipo: 'track',
        spotify_id: track.id,
        titulo: track.name,
        artista: track.artists.map(a => a.name).join(', '),
        album_nome: track.album?.name || '',
        capa_url: track.album?.images?.[0]?.url || '',
        duracao_ms: track.duration_ms,
        genero: '',
      }))
    } else if (searchType.value === 'album' && data.albums) {
      resultados.value = data.albums.items.map(album => ({
        tipo: 'album',
        spotify_id: album.id,
        titulo: album.name,
        artista: album.artists.map(a => a.name).join(', '),
        capa_url: album.images?.[0]?.url || '',
        ano: album.release_date ? parseInt(album.release_date.substring(0, 4)) : null,
        genero: '',
        total_tracks: album.total_tracks,
      }))
    }
  } catch (e) {
    mensagem.value = 'Erro de conexão com o servidor.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

const adicionarTrack = async (item) => {
  try {
    const response = await fetch(`${apiBase}/spotify/add-track/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        usuario_id: usuario.value.id,
        spotify_id: item.spotify_id,
        titulo: item.titulo,
        artista: item.artista,
        album_nome: item.album_nome,
        genero: item.genero,
        duracao_ms: item.duracao_ms,
        capa_url: item.capa_url,
      })
    })

    const data = await response.json()
    if (response.ok) {
      mensagem.value = response.status === 201
        ? `Música "${data.titulo}" adicionada!`
        : `Música "${data.titulo}" já existe no catálogo.`
    } else {
      mensagem.value = data.error || 'Erro ao adicionar música.'
    }
  } catch (e) {
    mensagem.value = 'Erro de conexão com o servidor.'
  }
}

const adicionarAlbum = async (item) => {
  try {
    const response = await fetch(`${apiBase}/spotify/add-album/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        usuario_id: usuario.value.id,
        spotify_id: item.spotify_id,
        titulo: item.titulo,
        artista: item.artista,
        ano: item.ano,
        genero: item.genero,
        capa_url: item.capa_url,
      })
    })

    const data = await response.json()
    if (response.ok) {
      mensagem.value = response.status === 201
        ? `Álbum "${data.titulo}" adicionado com ${data.faixas?.length || 0} faixas!`
        : `Álbum "${data.titulo}" já existe no catálogo.`
    } else {
      mensagem.value = data.error || 'Erro ao adicionar álbum.'
    }
  } catch (e) {
    mensagem.value = 'Erro de conexão com o servidor.'
  }
}
</script>

<template>
  <div class="admin-page">
    <HomeHeader />

    <div class="window admin-window">
      <div class="title-bar">
        <div class="title-bar-text">Admin - Buscar no Spotify</div>
        <div class="title-bar-controls">
          <button aria-label="Minimize"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close"></button>
        </div>
      </div>

      <div class="window-body">
        <form @submit.prevent="buscarSpotify" class="busca-form">
          <div class="field-row">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Nome da música ou álbum..."
              class="busca-input"
            />
            <select v-model="searchType">
              <option value="track">Música</option>
              <option value="album">Álbum</option>
            </select>
            <button type="submit" :disabled="loading">
              {{ loading ? 'Buscando...' : 'Buscar' }}
            </button>
          </div>
        </form>

        <div v-if="mensagem" class="mensagem">
          <p>{{ mensagem }}</p>
        </div>

        <div v-if="resultados.length" class="resultados">
          <div v-for="item in resultados" :key="item.spotify_id" class="resultado-item">
            <img v-if="item.capa_url" :src="item.capa_url" class="capa" :alt="item.titulo" />
            <div class="item-info">
              <strong>{{ item.titulo }}</strong>
              <span>{{ item.artista }}</span>
              <span v-if="item.album_nome" class="detalhe">Álbum: {{ item.album_nome }}</span>
              <span v-if="item.duracao_ms" class="detalhe">{{ formatarDuracao(item.duracao_ms) }}</span>
              <span v-if="item.ano" class="detalhe">{{ item.ano }}</span>
              <span v-if="item.total_tracks" class="detalhe">{{ item.total_tracks }} faixas</span>
            </div>
            <button
              v-if="item.tipo === 'track'"
              @click="adicionarTrack(item)"
              class="btn-adicionar"
            >
              Adicionar
            </button>
            <button
              v-else
              @click="adicionarAlbum(item)"
              class="btn-adicionar"
            >
              Adicionar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-self: flex-start;
  width: 100%;
  padding: 10px;
  min-height: 100vh;
  box-sizing: border-box;
}

.admin-window {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.busca-form {
  margin-bottom: 12px;
}

.field-row {
  display: flex;
  gap: 4px;
  align-items: center;
}

.busca-input {
  flex: 1;
}

.mensagem {
  padding: 8px;
  margin-bottom: 8px;
  border: 2px inset #fff;
  background: #fff;
  color: green;
  text-align: center;
  font-weight: bold;
}

.resultados {
  max-height: 500px;
  overflow-y: auto;
}

.resultado-item {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #ccc;
}

.capa {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border: 1px solid #000;
}

.item-info {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  flex: 1;
}

.detalhe {
  color: #666;
}

.btn-adicionar {
  min-width: 80px;
  align-self: center;
}
</style>
