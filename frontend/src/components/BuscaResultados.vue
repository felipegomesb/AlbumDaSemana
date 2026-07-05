<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()

const musicas = ref([])
const albuns = ref([])
const spotifyTracks = ref([])
const spotifyAlbums = ref([])
const generos = ref([])
const loading = ref(false)
const queryAtual = ref('')
const tipoFiltro = ref('todos')
const generoFiltro = ref('')
const ordenar = ref('recente')
const fonte = ref('posts')
const salvando = ref({})
const isMinimized = ref(false)
const isHeaderMinimized = ref(false)

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const buscarLocal = async (q) => {
  const params = new URLSearchParams()
  if (q) params.set('q', q)
  params.set('tipo', tipoFiltro.value)
  if (generoFiltro.value) params.set('genero', generoFiltro.value)
  params.set('ordenar', ordenar.value)

  const res = await fetch(`${apiBase}/busca/?${params.toString()}`)
  if (res.ok) {
    const data = await res.json()
    musicas.value = data.musicas || []
    albuns.value = data.albuns || []
    generos.value = data.generos || []
  }
}

const buscarSpotify = async (q) => {
  if (!q) {
    spotifyTracks.value = []
    spotifyAlbums.value = []
    return
  }

  if (tipoFiltro.value === 'album') {
    spotifyTracks.value = []
    const res = await fetch(`${apiBase}/busca/spotify/?q=${encodeURIComponent(q)}&type=album`)
    if (res.ok) {
      const data = await res.json()
      spotifyAlbums.value = (data.albums?.items || []).map(a => ({
        spotify_id: a.id,
        titulo: a.name,
        artista: a.artists?.map(ar => ar.name).join(', ') || '',
        ano: a.release_date ? parseInt(a.release_date) : null,
        capa_url: a.images?.[0]?.url || '',
        total_tracks: a.total_tracks || 0,
      }))
    }
  } else if (tipoFiltro.value === 'musica') {
    spotifyAlbums.value = []
    const res = await fetch(`${apiBase}/busca/spotify/?q=${encodeURIComponent(q)}&type=track`)
    if (res.ok) {
      const data = await res.json()
      spotifyTracks.value = (data.tracks?.items || []).map(t => ({
        spotify_id: t.id,
        titulo: t.name,
        artista: t.artists?.map(ar => ar.name).join(', ') || '',
        album_nome: t.album?.name || '',
        capa_url: t.album?.images?.[0]?.url || '',
        duracao_ms: t.duration_ms || 0,
      }))
    }
  } else {
    const [resTracks, resAlbums] = await Promise.all([
      fetch(`${apiBase}/busca/spotify/?q=${encodeURIComponent(q)}&type=track`),
      fetch(`${apiBase}/busca/spotify/?q=${encodeURIComponent(q)}&type=album`),
    ])
    if (resTracks.ok) {
      const data = await resTracks.json()
      spotifyTracks.value = (data.tracks?.items || []).map(t => ({
        spotify_id: t.id,
        titulo: t.name,
        artista: t.artists?.map(ar => ar.name).join(', ') || '',
        album_nome: t.album?.name || '',
        capa_url: t.album?.images?.[0]?.url || '',
        duracao_ms: t.duration_ms || 0,
      }))
    }
    if (resAlbums.ok) {
      const data = await resAlbums.json()
      spotifyAlbums.value = (data.albums?.items || []).map(a => ({
        spotify_id: a.id,
        titulo: a.name,
        artista: a.artists?.map(ar => ar.name).join(', ') || '',
        ano: a.release_date ? parseInt(a.release_date) : null,
        capa_url: a.images?.[0]?.url || '',
        total_tracks: a.total_tracks || 0,
      }))
    }
  }
}

const buscar = async () => {
  const q = route.query.q || ''
  queryAtual.value = q
  loading.value = true

  try {
    if (fonte.value === 'criar') {
      musicas.value = []
      albuns.value = []
      await buscarSpotify(q)
    } else {
      spotifyTracks.value = []
      spotifyAlbums.value = []
      await buscarLocal(q)
    }
  } catch (e) {
    console.error('Erro na busca:', e)
  } finally {
    loading.value = false
  }
}

const abrirTrack = async (track) => {
  const key = `track-${track.spotify_id}`
  salvando.value[key] = true
  try {
    const res = await fetch(`${apiBase}/musicas/garantir/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(track),
    })
    if (res.ok) {
      const musica = await res.json()
      router.push(`/musica/${musica.id}`)
    }
  } catch (e) {
    console.error('Erro ao salvar musica:', e)
  } finally {
    salvando.value[key] = false
  }
}

const abrirAlbum = async (album) => {
  const key = `album-${album.spotify_id}`
  salvando.value[key] = true
  try {
    const res = await fetch(`${apiBase}/albuns/garantir/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(album),
    })
    if (res.ok) {
      const albumLocal = await res.json()
      router.push(`/album/${albumLocal.id}`)
    }
  } catch (e) {
    console.error('Erro ao salvar album:', e)
  } finally {
    salvando.value[key] = false
  }
}

const totalResultados = () => {
  if (fonte.value === 'criar') return spotifyTracks.value.length + spotifyAlbums.value.length
  return musicas.value.length + albuns.value.length
}

onMounted(() => buscar())

watch(() => route.query.q, () => {
  generoFiltro.value = ''
  ordenar.value = 'recente'
  buscar()
})

watch([tipoFiltro, generoFiltro, ordenar, fonte], () => buscar())
</script>

<template>
  <div class="busca-page">
    <div v-if="isHeaderMinimized" class="window minimized-bar">
      <div class="title-bar">
        <div class="title-bar-text">AlbumDaSemana minimizado</div>
      </div>
      <div class="window-body minimized-body">
        <button type="button" @click="isHeaderMinimized = false">Restaurar</button>
      </div>
    </div>
    <HomeHeader v-else @minimize="isHeaderMinimized = true" />

    <div class="window resultados-window">
      <div class="title-bar">
        <div class="title-bar-text">
          Resultados{{ queryAtual ? ` para "${queryAtual}"` : '' }}
          <span v-if="!loading"> ({{ totalResultados() }})</span>
        </div>
        <div class="title-bar-controls">
          <button type="button" aria-label="Minimize" @click="isMinimized = !isMinimized"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close" @click="router.push('/')"></button>
        </div>
      </div>

      <div class="window-body" v-show="!isMinimized">
        <div class="fonte-botoes">
          <button :class="{ ativo: fonte === 'posts' }" @click="fonte = 'posts'">Buscar Posts</button>
          <button :class="{ ativo: fonte === 'criar' }" @click="fonte = 'criar'">Criar Novo</button>
        </div>

        <fieldset class="filtros">
          <legend>Filtros</legend>
          <div class="filtros-row">
            <div class="filtro-grupo">
              <label>Tipo:</label>
              <select v-model="tipoFiltro">
                <option value="todos">Todos</option>
                <option value="musica">Musicas</option>
                <option value="album">Albuns</option>
              </select>
            </div>

            <div v-if="fonte === 'posts'" class="filtro-grupo">
              <label>Genero:</label>
              <select v-model="generoFiltro">
                <option value="">Todos</option>
                <option v-for="g in generos" :key="g" :value="g">{{ g }}</option>
              </select>
            </div>

            <div v-if="fonte === 'posts'" class="filtro-grupo">
              <label>Ordenar:</label>
              <select v-model="ordenar">
                <option value="recente">Mais recentes</option>
                <option value="likes">Mais curtidos</option>
                <option value="titulo">A-Z</option>
              </select>
            </div>
          </div>
        </fieldset>

        <div v-if="loading" class="loading">Buscando...</div>

        <div v-else>
          <!-- CRIAR NOVO (Spotify) -->
          <template v-if="fonte === 'criar'">
            <div v-if="!spotifyTracks.length && !spotifyAlbums.length && queryAtual" class="vazio">
              Nenhum resultado encontrado.
            </div>

            <div v-if="spotifyTracks.length" class="secao">
              <div class="secao-header">
                <h3>Musicas ({{ spotifyTracks.length }})</h3>
              </div>
              <table class="resultado-tabela">
                <thead>
                  <tr>
                    <th class="col-capa"></th>
                    <th>Titulo</th>
                    <th>Artista</th>
                    <th>Album</th>
                    <th>Duracao</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="t in spotifyTracks" :key="t.spotify_id">
                    <td class="col-capa">
                      <img v-if="t.capa_url" :src="t.capa_url" class="mini-capa" :alt="t.titulo" />
                    </td>
                    <td><strong>{{ t.titulo }}</strong></td>
                    <td>{{ t.artista }}</td>
                    <td>{{ t.album_nome }}</td>
                    <td>{{ t.duracao_ms ? formatarDuracao(t.duracao_ms) : '-' }}</td>
                    <td>
                      <button
                        :disabled="salvando[`track-${t.spotify_id}`]"
                        @click="abrirTrack(t)"
                      >
                        {{ salvando[`track-${t.spotify_id}`] ? '...' : 'Avaliar' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="spotifyAlbums.length" class="secao">
              <div class="secao-header">
                <h3>Albuns ({{ spotifyAlbums.length }})</h3>
              </div>
              <table class="resultado-tabela">
                <thead>
                  <tr>
                    <th class="col-capa"></th>
                    <th>Titulo</th>
                    <th>Artista</th>
                    <th>Ano</th>
                    <th>Faixas</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in spotifyAlbums" :key="a.spotify_id">
                    <td class="col-capa">
                      <img v-if="a.capa_url" :src="a.capa_url" class="mini-capa" :alt="a.titulo" />
                    </td>
                    <td><strong>{{ a.titulo }}</strong></td>
                    <td>{{ a.artista }}</td>
                    <td>{{ a.ano || '-' }}</td>
                    <td>{{ a.total_tracks || '-' }}</td>
                    <td>
                      <button
                        :disabled="salvando[`album-${a.spotify_id}`]"
                        @click="abrirAlbum(a)"
                      >
                        {{ salvando[`album-${a.spotify_id}`] ? '...' : 'Avaliar' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

          <!-- BUSCAR POSTS (local) -->
          <template v-else>
            <div v-if="!musicas.length && !albuns.length" class="vazio">
              Nenhum resultado encontrado.
            </div>

            <div v-if="musicas.length" class="secao">
              <div class="secao-header">
                <h3>Musicas ({{ musicas.length }})</h3>
              </div>
              <table class="resultado-tabela">
                <thead>
                  <tr>
                    <th class="col-capa"></th>
                    <th>Titulo</th>
                    <th>Artista</th>
                    <th>Genero</th>
                    <th>Duracao</th>
                    <th>Likes</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="m in musicas" :key="m.id">
                    <td class="col-capa">
                      <img v-if="m.capa_url" :src="m.capa_url" class="mini-capa" :alt="m.titulo" />
                    </td>
                    <td><strong>{{ m.titulo }}</strong></td>
                    <td>{{ m.artista }}</td>
                    <td>
                      <span v-if="m.genero" class="tag-genero">{{ m.genero }}</span>
                    </td>
                    <td>{{ m.duracao_ms ? formatarDuracao(m.duracao_ms) : '-' }}</td>
                    <td>{{ m.likes || 0 }}</td>
                    <td>
                      <button @click="router.push(`/musica/${m.id}`)">Ver</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="albuns.length" class="secao">
              <div class="secao-header">
                <h3>Albuns ({{ albuns.length }})</h3>
              </div>
              <table class="resultado-tabela">
                <thead>
                  <tr>
                    <th class="col-capa"></th>
                    <th>Titulo</th>
                    <th>Artista</th>
                    <th>Ano</th>
                    <th>Genero</th>
                    <th>Likes</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in albuns" :key="a.id">
                    <td class="col-capa">
                      <img v-if="a.capa_url" :src="a.capa_url" class="mini-capa" :alt="a.titulo" />
                    </td>
                    <td><strong>{{ a.titulo }}</strong></td>
                    <td>{{ a.artista }}</td>
                    <td>{{ a.ano || '-' }}</td>
                    <td>
                      <span v-if="a.genero" class="tag-genero">{{ a.genero }}</span>
                    </td>
                    <td>{{ a.likes || 0 }}</td>
                    <td>
                      <button @click="router.push(`/album/${a.id}`)">Ver</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.busca-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-self: flex-start;
  width: 100%;
  padding: 10px;
  min-height: 100vh;
  box-sizing: border-box;
}

.resultados-window {
  width: 100%;
  max-width: 900px;
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

.fonte-botoes {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
}

.fonte-botoes button {
  flex: 1;
  padding: 6px 12px;
  font-size: 13px;
  cursor: pointer;
}

.fonte-botoes button.ativo {
  font-weight: bold;
  box-shadow: inset 1px 1px 2px #000;
}

.filtros {
  margin-bottom: 12px;
}

.filtros-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: center;
}

.filtro-grupo {
  display: flex;
  align-items: center;
  gap: 4px;
}

.filtro-grupo label {
  font-size: 12px;
  white-space: nowrap;
}

.filtro-grupo select {
  font-size: 12px;
}

.secao {
  margin-bottom: 16px;
}

.secao-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #000;
  margin-bottom: 4px;
}

.secao-header h3 {
  margin: 4px 0;
  font-size: 14px;
}

.resultado-tabela {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.resultado-tabela th {
  text-align: left;
  padding: 4px 6px;
  background: #c0c0c0;
  border: 1px solid #808080;
  font-size: 11px;
}

.resultado-tabela td {
  padding: 4px 6px;
  border-bottom: 1px solid #dfdfdf;
  vertical-align: middle;
}

.resultado-tabela tbody tr:hover {
  background: #000080;
  color: #fff;
}

.col-capa {
  width: 40px;
}

.mini-capa {
  width: 36px;
  height: 36px;
  object-fit: cover;
  border: 1px solid #808080;
}

.tag-genero {
  background: #c0c0c0;
  border: 1px solid #808080;
  padding: 1px 6px;
  font-size: 11px;
}

.loading, .vazio {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>
