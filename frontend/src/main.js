import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import LoginSimples from './components/loginSimples.vue'
import CadastroSimples from './components/cadastroSimples.vue'
import router from './router'
import './style.css'
const app = createApp(App)

app.use(router) // Diz para o Vue usar o sistema de rotas
app.mount('#app')


