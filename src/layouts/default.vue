<template>
  <v-main>
    
  </v-main>

  <AppFooter />
  <v-app-bar>
    <v-app-bar-title>
      Simple Local Gallery:
      <v-btn density="compact" icon="mdi-home-edit" @click="resetGalleryRoot"></v-btn>
      {{ galleryRoot?.data ?? 'Not Set' }}
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
import { useMutation, useQuery, useQueryCache } from '@pinia/colada';
import { getGalleryRootQuery, resetGalleryRootMutation } from '@/slg-api/@pinia/colada/settings.gen';

const queryCache = useQueryCache()

const { state: galleryRoot } = useQuery({...getGalleryRootQuery()})
const { mutate: resetGalleryRoot } = useMutation({
  ...resetGalleryRootMutation(),
  onSettled: () => queryCache.invalidateQueries()
})
</script>
