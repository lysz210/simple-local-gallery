<template>
  <v-main>
    
  </v-main>

  <AppFooter />
  <v-app-bar>
    <v-app-bar-title>
      Simple Local Gallery:
      <v-btn density="compact" icon="mdi-home-edit" @click="resetGalleryRoot"></v-btn>
      {{ galleryRoot ?? 'Not Set' }}
    </v-app-bar-title>
  </v-app-bar>

  <GalleryDrawer />

  <v-main class="d-flex align-center justify-center" height="300">
    <router-view />
  </v-main>
  <PiniaColadaDevtools  />
</template>

<script lang="ts" setup>
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { Photos, Settings } from '@/slg-api';


const galleryRoot: Ref<string|null> = ref('')

Settings.getGalleryRoot().then(res => {
  galleryRoot.value = res.data ?? null
})

async function resetGalleryRoot() {
  
  const res = await Settings.resetGalleryRoot()
  galleryRoot.value = res.data ?? null
  window.location.reload()
}
</script>
