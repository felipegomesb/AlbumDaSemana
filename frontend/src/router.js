import { createRouter, createWebHistory } from 'vue-router'

// Usando o '@', o Vite vai direto na pasta 'src' procurar a pasta 'components'
import Login from './components/loginSimples.vue'
import Cadastro from './components/cadastroSimples.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/cadastro',
    name: 'Cadastro',
    component: Cadastro
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router