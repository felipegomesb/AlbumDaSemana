import { createRouter, createWebHistory } from 'vue-router'

import Login from './components/loginSimples.vue'
import Cadastro from './components/cadastroSimples.vue'
import HomePage from './components/HomePage.vue'
import BuscaResultados from './components/BuscaResultados.vue'
import AdminSpotify from './components/adminSpotify.vue'
import Perfil from './components/Perfil.vue'
import DetalheMusica from './components/DetalheMusica.vue'
import DetalheAlbum from './components/DetalheAlbum.vue'

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
    path: '/musica/:id',
    name: 'DetalheMusica',
    component: DetalheMusica
  },
  {
    path: '/album/:id',
    name: 'DetalheAlbum',
    component: DetalheAlbum
  },
  {
    path: '/admin-spotify',
    name: 'AdminSpotify',
    component: AdminSpotify
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: Perfil
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
