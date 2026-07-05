<script setup>
import { ref, onMounted } from 'vue'

const apiBase = import.meta.env.VITE_API_BASE_URL
const musicas = ref([])
const loading = ref(true)
const erro = ref('')
const isMinimized = ref(false)

const formatarData = (dataStr) => {
  const data = new Date(dataStr)
  return data.toLocaleDateString('pt-BR')
}

const formatarDuracao = (ms) => {
  const minutos = Math.floor(ms / 60000)
  const segundos = Math.floor((ms % 60000) / 1000)
  return `${minutos}:${segundos.toString().padStart(2, '0')}`
}

onMounted(async () => {
  try {
    const response = await fetch(`${apiBase}/musicas/`)

    if (!response.ok) {
      throw new Error('Falha ao carregar músicas recentes')
    }

    const data = await response.json()
    musicas.value = data.slice(0, 5)
  } catch (e) {
    erro.value = 'Não foi possível carregar as músicas recentes.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="window recentes-window">
    <div class="title-bar">
      <div class="title-bar-text">Músicas Recentes</div>
      <div class="title-bar-controls">
        <button type="button" aria-label="Minimize" @click="isMinimized = !isMinimized"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body" v-show="!isMinimized">
      <div v-if="loading" class="estado">Carregando...</div>

      <div v-else-if="erro" class="estado">{{ erro }}</div>

      <div v-else-if="musicas.length" class="recentes-layout">
        <div class="destaque" :class="{ vazio: !musicas[0] }">
          <div class="destaque-label">Última música adicionada</div>
          <template v-if="musicas[0]">
            <img
              v-if="musicas[0].capa_url"
              :src="musicas[0].capa_url"
              :alt="musicas[0].titulo"
              class="destaque-capa"
            />
            <div class="destaque-info">
              <strong>{{ musicas[0].titulo }}</strong>
              <span>{{ musicas[0].artista }}</span>
              <span v-if="musicas[0].album_nome">Álbum: {{ musicas[0].album_nome }}</span>
              <span v-if="musicas[0].duracao_ms">Duração: {{ formatarDuracao(musicas[0].duracao_ms) }}</span>
              <span class="data">Adicionada em {{ formatarData(musicas[0].criado_em) }}</span>
            </div>
          </template>
        </div>

        <div class="lista-recente">
          <div
            v-for="musica in musicas.slice(1)"
            :key="musica.id"
            class="musica-item"
          >
            <div class="musica-texto">
              <strong>{{ musica.titulo }}</strong>
              <span>{{ musica.artista }}</span>
            </div>
            <div class="musica-meta">
              <span v-if="musica.album_nome">{{ musica.album_nome }}</span>
              <span v-if="musica.criado_em">{{ formatarData(musica.criado_em) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="estado">Nenhuma música cadastrada ainda.</div>
    </div>
  </div>
</template>

<style scoped>
.recentes-window {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.estado {
  text-align: center;
  padding: 16px;
  color: #666;
}

.recentes-layout {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 12px;
  align-items: start;
}

.destaque {
  position: relative;
  padding: 12px;
  border: 2px inset #fff;
  background: #fff;
  display: flex;
  gap: 12px;
  min-height: 160px;
}

.destaque-label {
  position: absolute;
  transform: translateY(-24px);
  font-size: 12px;
  background: #d6d6d6;
  padding: 0 6px;
}

.destaque-capa {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border: 1px solid #000;
}

.destaque-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
}

.data {
  color: #666;
}

.lista-recente {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.musica-item {
  padding: 8px;
  border-bottom: 1px solid #ccc;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.musica-texto,
.musica-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 13px;
}

.musica-meta {
  align-items: flex-end;
  color: #666;
}

@media (max-width: 700px) {
  .recentes-layout {
    grid-template-columns: 1fr;
  }

  .destaque {
    flex-direction: column;
  }

  .destaque-label {
    position: static;
    transform: none;
    display: inline-block;
    margin-bottom: 4px;
  }
}
</style>