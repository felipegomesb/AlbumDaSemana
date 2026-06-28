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

// funcao login
const Login = async () => {
  loading.value = true
  success.value = false

  try {
    // 1. Fazemos a requisição para o backend
    const response = await fetch(`${apiBase}/data/login/`, {
      method: 'POST', // Método para criar dados
      headers: {
        'Content-Type': 'application/json' // Avisa o backend que estamos enviando JSON
      },
      body: JSON.stringify(form.value) // Transforma os dados do formulário em texto JSON
    })

    // 2. Verificamos se o backend retornou algum erro (ex: 400 ou 500)
    if (!response.ok) {
      throw new Error('Erro ao realizar login no servidor.')
    }

    // 3. Se deu tudo certo, mostramos a mensagem e limpamos o formulário
    success.value = true
    form.value = { user_email: '', user_password: '' }
    
  } catch (error) {
    console.error('Erro no login:', error)
    alert('Falha ao realizar login. Verifique o console.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="window container">
    
    <div class="title-bar">
      <div class="title-bar-text">Login</div>
      <div class="title-bar-controls">
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body">
      <form @submit.prevent="Login">
        
        <div class="field-row-stacked">
          <label for="email">E-mail:</label>
          <input v-model="form.user_email" id="email" type="email" required />
        </div>
        
        <div class="field-row-stacked">
          <label for="password">Senha:</label>
          <input v-model="form.user_password" id="password" type="password" required />
        </div>
        
        <div class="field-row-stacked">
          <p>Não tem conta? <router-link to="/cadastro">Cadastre-se aqui</router-link></p>
        </div>

        <div class="actions">
          <button type="submit" :disabled="loading">
            {{ loading ? 'Aguarde...' : 'Login' }}
          </button>
        </div>

      </form>
      
      <div v-if="success" class="status-box">
        <p>Usuário logado com sucesso!</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* Estilos extras apenas para posicionamento, já que o 98.css cuida do visual */
.container {
  width: 350px;
  margin: 0 auto;
}

.field-row-stacked {
  margin-bottom: 14px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

button[type="submit"] {
  min-width: 80px;
}

.status-box {
  margin-top: 15px;
  padding: 10px;
  border: 2px inset #fff;
  background: #fff;
  color: green;
  text-align: center;
  font-weight: bold;
}
</style>