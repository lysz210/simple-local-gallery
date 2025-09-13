<template>
  <v-app-bar>
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="galleryDrawerOpen = !galleryDrawerOpen"></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>
      Simple Local Gallery:
      <v-btn density="compact" icon="mdi-home-edit" @click="resetGalleryRoot"></v-btn>
      {{ galleryRoot?.data ?? 'Not Set' }}
    </v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer app v-model="galleryDrawerOpen">
    <GalleryDrawerContent />
  </v-navigation-drawer>

  <v-main class="d-flex align-start justify-center">
    <router-view />
  </v-main>
  <PiniaColadaDevtools  />
</template>

<script lang="ts" setup>
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada';
import { getGalleryRootQuery, resetGalleryRootMutation } from '@/slg-api/@pinia/colada/settings.gen';

const galleryDrawerOpen = ref(true)

const queryCache = useQueryCache()

const { state: galleryRoot } = useQuery({...getGalleryRootQuery()})
const { mutate: resetGalleryRoot } = useMutation({
  ...resetGalleryRootMutation(),
  onSettled: () => queryCache.invalidateQueries()
})
</script>
