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
  align-self: flex-start;
  width: 100%;
  padding: 10px;
  min-height: 100vh;
  box-sizing: border-box;
}
</style>
