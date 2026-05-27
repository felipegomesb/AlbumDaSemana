<script setup>
import { ref, onMounted } from 'vue'

// Variáveis de ambiente
const apiBase = import.meta.env.VITE_API_BASE_URL

// Estado do componente
const users = ref([])
const loading = ref(false)
const success = ref(false)

// Dados do formulário
const form = ref({
  user_username: '',
  user_email: '',
  user_password: ''
})

// Buscar usuários ao carregar a página
onMounted(async () => {
  try {
    const response = await fetch(`${apiBase}/data/`)
    users.value = await response.json()
  } catch (error) {
    console.error('Erro ao buscar usuários:', error)
  }
})

// Função para registrar o usuário (AQUI ACONTECE A CONEXÃO REAL)
const registrar = async () => {
  loading.value = true
  success.value = false

  try {
    // 1. Fazemos a requisição para o backend
    const response = await fetch(`${apiBase}/data/`, {
      method: 'POST', // Método para criar dados
      headers: {
        'Content-Type': 'application/json' // Avisa o backend que estamos enviando JSON
      },
      body: JSON.stringify(form.value) // Transforma os dados do formulário em texto JSON
    })

    // 2. Verificamos se o backend retornou algum erro (ex: 400 ou 500)
    if (!response.ok) {
      throw new Error('Erro ao cadastrar usuário no servidor.')
    }

    // 3. Se deu tudo certo, mostramos a mensagem e limpamos o formulário
    success.value = true
    form.value = { user_username: '', user_email: '', user_password: '' }
    
  } catch (error) {
    console.error('Erro no cadastro:', error)
    alert('Falha ao cadastrar. Verifique o console.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <h2>Cadastro de Usuário</h2>
    <form @submit.prevent="registrar">
      <div>
        <label>Nome:</label>
        <input v-model="form.user_username" type="text" required />
      </div>
      <div>
        <label>E-mail:</label>
        <input v-model="form.user_email" type="email" required />
      </div>
      <div>
        <label>Senha:</label>
        <input v-model="form.user_password" type="password" required />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Cadastrando...' : 'Cadastrar' }}
      </button>
    </form>
    <p v-if="success" class="success">Usuário cadastrado com sucesso!</p>
  </div>
</template>

<style scoped>
.container { max-width: 400px; margin: 2rem auto; padding: 1rem; }
div { margin-bottom: 1rem; }
input { width: 100%; padding: 0.5rem; }
button { width: 100%; padding: 0.5rem; background: #007bff; color: white; border: none; cursor: pointer; }
button:disabled { background: #ccc; }
.success { color: green; margin-top: 1rem; }
</style>