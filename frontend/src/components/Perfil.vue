<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import HomeHeader from './HomeHeader.vue'

const router = useRouter()
const usuario = ref(null)

const carregarUsuario = () => {
  const savedUser = localStorage.getItem('albumDaSemanaUser')
  usuario.value = savedUser ? JSON.parse(savedUser) : null
}

const sair = () => {
  localStorage.removeItem('albumDaSemanaUser')
  window.dispatchEvent(new Event('album-user-changed'))
  router.push('/login')
}

const temUsuario = computed(() => Boolean(usuario.value))

onMounted(() => {
  carregarUsuario()
})
</script>

<template>
  <div class="perfil-page">
    <HomeHeader />

    <div class="window perfil-window">
      <div class="title-bar">
        <div class="title-bar-text">Tela de Perfil</div>
        <div class="title-bar-controls">
          <button aria-label="Minimize"></button>
          <button aria-label="Maximize"></button>
          <button aria-label="Close"></button>
        </div>
      </div>

      <div class="window-body">
        <div v-if="temUsuario" class="perfil-conteudo">
          <div class="perfil-header">
            <div class="avatar">{{ usuario.user_username?.charAt(0)?.toUpperCase() }}</div>
            <div>
              <h2>{{ usuario.user_username }}</h2>
              <p>{{ usuario.user_email }}</p>
            </div>
          </div>

          <div class="perfil-dados">
            <div class="field-row-stacked">
              <label>ID</label>
              <input :value="usuario.id" readonly />
            </div>
            <div class="field-row-stacked">
              <label>Usuário</label>
              <input :value="usuario.user_username" readonly />
            </div>
            <div class="field-row-stacked">
              <label>E-mail</label>
              <input :value="usuario.user_email" readonly />
            </div>
          </div>

          <div class="actions">
            <button type="button" @click="sair">Sair</button>
          </div>
        </div>

        <div v-else class="sem-sessao">
          <p>Nenhum usuário autenticado.</p>
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
  max-width: 900px;
  margin: 10px auto;
}

.perfil-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #d6d6d6;
  border: 2px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
}

.perfil-dados {
  display: grid;
  gap: 12px;
}

.field-row-stacked {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.sem-sessao {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}
</style>