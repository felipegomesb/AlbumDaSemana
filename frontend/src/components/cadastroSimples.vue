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
  <div class="window container">
    
    <div class="title-bar">
      <div class="title-bar-text">Cadastro de Usuário</div>
      <div class="title-bar-controls">
        <button aria-label="Minimize"></button>
        <button aria-label="Maximize"></button>
        <button aria-label="Close"></button>
      </div>
    </div>

    <div class="window-body">
      <form @submit.prevent="registrar">
        
        <div class="field-row-stacked">
          <label for="username">Nome:</label>
          <input v-model="form.user_username" id="username" type="text" required />
        </div>
        
        <div class="field-row-stacked">
          <label for="email">E-mail:</label>
          <input v-model="form.user_email" id="email" type="email" required />
        </div>
        
        <div class="field-row-stacked">
          <label for="password">Senha:</label>
          <input v-model="form.user_password" id="password" type="password" required />
        </div>
        
        <div class="actions">
          <button type="submit" :disabled="loading">
            {{ loading ? 'Aguarde...' : 'Cadastrar' }}
          </button>
        </div>

      </form>
      
      <div v-if="success" class="status-box">
        <p>Usuário cadastrado com sucesso!</p>
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