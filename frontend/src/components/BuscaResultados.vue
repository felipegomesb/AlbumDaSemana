<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import HomeHeader from './HomeHeader.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const route = useRoute()

const musicas = ref([])
const albuns = ref([])
const loading = ref(false)
const queryAtual = ref('')

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

const buscar = async (q) => {
  if (!q) return
  queryAtual.value = q
  loading.value = true

  try {
    const response = await fetch(`${apiBase}/busca/?q=${encodeURIComponent(q)}`)
    if (response.ok) {
      const data = await response.json()
      musicas.value = data.musicas || []
      albuns.value = data.albuns || []
    }
  } catch (e) {
    console.error('Erro na busca:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (route.query.q) buscar(route.query.q)
})

watch(() => route.query.q, (newQ) => {
  if (newQ) buscar(newQ)
})
</script>

<template>
  <div class="busca-page">
    <HomeHeader />

    <div class="window resultados-window">
      <div class="title-bar">
        <div class="title-bar-text">Resultados para "{{ queryAtual }}"</div>
        <div class="title-bar-controls">
          <button aria-label="Minimize"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close"></button>
        </div>
      </div>

      <div class="window-body">
        <div v-if="loading" class="loading">Buscando...</div>

        <div v-else>
          <div v-if="!musicas.length && !albuns.length && queryAtual" class="vazio">
            Nenhum resultado encontrado.
          </div>

          <div v-if="musicas.length" class="secao">
            <h3>Músicas</h3>
            <div v-for="m in musicas" :key="m.id" class="resultado-item">
              <img v-if="m.capa_url" :src="m.capa_url" class="mini-capa" :alt="m.titulo" />
              <div class="resultado-info">
                <strong>{{ m.titulo }}</strong>
                <span>{{ m.artista }}</span>
                <span v-if="m.duracao_ms" class="detalhe">{{ formatarDuracao(m.duracao_ms) }}</span>
              </div>
            </div>
          </div>

          <div v-if="albuns.length" class="secao">
            <h3>Álbuns</h3>
            <div v-for="a in albuns" :key="a.id" class="resultado-item">
              <img v-if="a.capa_url" :src="a.capa_url" class="mini-capa" :alt="a.titulo" />
              <div class="resultado-info">
                <strong>{{ a.titulo }}</strong>
                <span>{{ a.artista }}</span>
                <span v-if="a.ano" class="detalhe">{{ a.ano }}</span>
              </div>
            </div>
          </div>
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
  padding: 10px;
  min-height: 100vh;
}

.resultados-window {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.secao {
  margin-bottom: 16px;
}

.secao h3 {
  margin: 8px 0;
  font-size: 14px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 4px;
}

.resultado-item {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #eee;
}

.mini-capa {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border: 1px solid #000;
}

.resultado-info {
  display: flex;
  flex-direction: column;
  font-size: 13px;
}

.detalhe {
  color: #666;
}

.loading, .vazio {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>
