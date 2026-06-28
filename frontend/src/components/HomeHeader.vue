<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

const buscar = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/busca', query: { q: searchQuery.value.trim() } })
  }
}
</script>

<template>
  <div class="window header-window">
    <div class="title-bar">
      <div class="title-bar-text">AlbumDaSemana</div>
      <div class="title-bar-controls">
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body header-body">
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/login">Login</router-link>
        <router-link to="/cadastro">Cadastro</router-link>
        <router-link to="/admin-spotify">Admin Spotify</router-link>
      </div>

      <form class="search-form" @submit.prevent="buscar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar músicas e álbuns..."
          class="search-input"
        />
        <button type="submit">Buscar</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.header-window {
  width: 100%;
  max-width: 900px;
  margin: 10px auto;
}

.header-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.nav-links {
  display: flex;
  gap: 12px;
  align-items: center;
}

.nav-links a {
  color: #000;
  text-decoration: none;
  font-size: 14px;
}

.nav-links a:hover {
  text-decoration: underline;
}

.nav-links a.router-link-active {
  font-weight: bold;
}

.search-form {
  display: flex;
  gap: 4px;
  align-items: center;
}

.search-input {
  width: 200px;
}
</style>
