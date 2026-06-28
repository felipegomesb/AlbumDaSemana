import { createRouter, createWebHistory } from 'vue-router'

import Login from './components/loginSimples.vue'
import Cadastro from './components/cadastroSimples.vue'
import HomePage from './components/HomePage.vue'
import BuscaResultados from './components/BuscaResultados.vue'
import AdminSpotify from './components/adminSpotify.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/cadastro',
    name: 'Cadastro',
    component: Cadastro
  },
  {
    path: '/busca',
    name: 'Busca',
    component: BuscaResultados
  },
  {
    path: '/admin-spotify',
    name: 'AdminSpotify',
    component: AdminSpotify
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
