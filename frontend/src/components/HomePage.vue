<script setup>
import HomeHeader from './HomeHeader.vue'
import MusicaDoDiaCard from './MusicaDoDiaCard.vue'
import AlbumDaSemanaCard from './AlbumDaSemanaCard.vue'
import HistoricoSection from './HistoricoSection.vue'
</script>

<template>
  <div class="home-page">
    <HomeHeader />
    <MusicaDoDiaCard />
    <AlbumDaSemanaCard />
    <HistoricoSection />
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  min-height: 100vh;
}
</style>
