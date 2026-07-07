<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'

const router = useRouter()
const apiBase = import.meta.env.VITE_API_BASE_URL

const topAlbuns = ref([])
const topMusicas = ref([])
const topArtistas = ref([])
const loading = ref(true)
const erro = ref('')

const albunsMinimized = ref(false)
const musicasMinimized = ref(false)
const artistasMinimized = ref(false)

const formatarNota = (item) => {
  if (item.nota_media != null) return item.nota_media + '/5'
  return '-'
}

onMounted(async () => {
  try {
    const res = await fetch(`${apiBase}/rankings/`)
    if (!res.ok) throw new Error('Falha ao carregar rankings')
    const data = await res.json()
    topAlbuns.value = data.top_albuns
    topMusicas.value = data.top_musicas
    topArtistas.value = data.top_artistas
  } catch (e) {
    erro.value = 'Nenhum dado de ranking disponivel ainda.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="rankings-page">
    <HomeHeader />

    <div v-if="loading" class="window rankings-window">
      <div class="title-bar">
        <div class="title-bar-text">Rankings</div>
      </div>
      <div class="window-body loading-body">Carregando...</div>
    </div>

    <div v-else-if="erro && !topAlbuns.length && !topMusicas.length && !topArtistas.length" class="window rankings-window">
      <div class="title-bar">
        <div class="title-bar-text">Rankings</div>
      </div>
      <div class="window-body loading-body">{{ erro }}</div>
    </div>

    <template v-else>
      <div v-if="topAlbuns.length" class="window rankings-window">
        <div class="title-bar">
          <div class="title-bar-text">Top Albums Avaliados</div>
          <div class="title-bar-controls">
            <button type="button" aria-label="Minimize" @click="albunsMinimized = !albunsMinimized"></button>
            <button aria-label="Maximize"></button>
            <button aria-label="Close"></button>
          </div>
        </div>
        <div class="window-body" v-show="!albunsMinimized">
          <table class="ranking-table">
            <thead>
              <tr>
                <th>#</th>
                <th></th>
                <th>Album</th>
                <th>Artista</th>
                <th>Nota</th>
                <th>Posts</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(album, i) in topAlbuns"
                :key="album.id"
                class="ranking-row"
                @click="router.push({ name: 'DetalheAlbum', params: { id: album.id } })"
              >
                <td class="rank">{{ i + 1 }}</td>
                <td>
                  <img v-if="album.capa_url" :src="album.capa_url" :alt="album.titulo" class="mini-capa" />
                </td>
                <td>{{ album.titulo }}</td>
                <td>{{ album.artista }}</td>
                <td>
                  <span class="estrelas">
                    <span v-for="n in 5" :key="n" :class="{ preenchida: n <= Math.round(album.nota_media || 0) }">★</span>
                  </span>
                  <span class="nota-valor">{{ formatarNota(album) }}</span>
                </td>
                <td>{{ album.review_count || 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="topMusicas.length" class="window rankings-window">
        <div class="title-bar">
          <div class="title-bar-text">Top Musicas Avaliadas</div>
          <div class="title-bar-controls">
            <button type="button" aria-label="Minimize" @click="musicasMinimized = !musicasMinimized"></button>
            <button aria-label="Maximize"></button>
            <button aria-label="Close"></button>
          </div>
        </div>
        <div class="window-body" v-show="!musicasMinimized">
          <table class="ranking-table">
            <thead>
              <tr>
                <th>#</th>
                <th></th>
                <th>Musica</th>
                <th>Artista</th>
                <th>Nota</th>
                <th>Posts</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(musica, i) in topMusicas"
                :key="musica.id"
                class="ranking-row"
                @click="router.push({ name: 'DetalheMusica', params: { id: musica.id } })"
              >
                <td class="rank">{{ i + 1 }}</td>
                <td>
                  <img v-if="musica.capa_url" :src="musica.capa_url" :alt="musica.titulo" class="mini-capa" />
                </td>
                <td>{{ musica.titulo }}</td>
                <td>{{ musica.artista }}</td>
                <td>
                  <span class="estrelas">
                    <span v-for="n in 5" :key="n" :class="{ preenchida: n <= Math.round(musica.nota_media || 0) }">★</span>
                  </span>
                  <span class="nota-valor">{{ formatarNota(musica) }}</span>
                </td>
                <td>{{ musica.review_count || 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="topArtistas.length" class="window rankings-window">
        <div class="title-bar">
          <div class="title-bar-text">Artistas Mais Avaliados</div>
          <div class="title-bar-controls">
            <button type="button" aria-label="Minimize" @click="artistasMinimized = !artistasMinimized"></button>
            <button aria-label="Maximize"></button>
            <button aria-label="Close"></button>
          </div>
        </div>
        <div class="window-body" v-show="!artistasMinimized">
          <table class="ranking-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Artista</th>
                <th>Total de Reviews</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(artista, i) in topArtistas" :key="artista.artista" class="ranking-row-static">
                <td class="rank">{{ i + 1 }}</td>
                <td>{{ artista.artista }}</td>
                <td>{{ artista.total_reviews }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.rankings-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-self: flex-start;
  width: 100%;
  padding: 10px;
  min-height: 100vh;
  box-sizing: border-box;
}

.rankings-window {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.loading-body {
  text-align: center;
  padding: 20px;
  color: #666;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.ranking-table th,
.ranking-table td {
  text-align: left;
  padding: 6px 8px;
  border-bottom: 1px solid #ccc;
}

.ranking-table th {
  background: #dfdfdf;
}

.ranking-row {
  cursor: pointer;
}

.ranking-row:hover {
  background: #000080;
  color: #fff;
}

.ranking-row-static {
  cursor: default;
}

.ranking-row-static:hover {
  background: #e8e8e8;
}

.rank {
  font-weight: bold;
  width: 30px;
  text-align: center;
}

.mini-capa {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border: 1px solid #000;
  vertical-align: middle;
}

.estrelas {
  font-size: 13px;
  color: #bbb;
  letter-spacing: 1px;
}

.estrelas span.preenchida {
  color: #d4a017;
}

.nota-valor {
  font-size: 11px;
  color: #666;
  margin-left: 4px;
}

.ranking-row:hover .nota-valor {
  color: #ccc;
}

.ranking-row:hover .estrelas {
  color: #888;
}

.ranking-row:hover .estrelas span.preenchida {
  color: #ffd700;
}
</style>
