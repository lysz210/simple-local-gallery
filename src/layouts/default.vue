<template>
  <v-app-bar>
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="galleryDrawerOpen = !galleryDrawerOpen"></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>
      Simple Local Gallery:
      {{ galleryRoot?.data ?? 'Not Set' }}
      <v-btn density="compact" icon="mdi-pencil" @click="resetGalleryRoot"></v-btn>
    </v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer app v-model="galleryDrawerOpen">
    <GalleryDrawerContent />
  </v-navigation-drawer>

  <v-main class="d-flex align-start justify-center">
    <router-view />
  </v-main>
  <v-footer
    app
    class="overflow-x-auto ga-2"
    v-if="fsStore.previewSelecetedPhotos"
  >
    <template
      v-for="(photos, folder) in fsStore.selectedPhotos" :key="folder"
    >
      <img
        v-for="photo in photos" :key="photo"
        :src="`http://localhost:8000/thumbnails/${photo}`"
        height="180px"
        @click="removeSelectedPhoto(folder, photo)"
      ></img>
    </template>
  </v-footer>
  <PiniaColadaDevtools  />
</template>

<script lang="ts" setup>
import { PiniaColadaDevtools } from '@pinia/colada-devtools'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada';
import { getGalleryRootQuery, resetGalleryRootMutation } from '@/slg-api/@pinia/colada/settings.gen';
import { useFsStore } from '@/stores/fs';

const galleryDrawerOpen = ref(true)

const queryCache = useQueryCache()

const { state: galleryRoot } = useQuery({...getGalleryRootQuery()})
const { mutate: resetGalleryRoot } = useMutation({
  ...resetGalleryRootMutation(),
  onSettled: () => {
    queryCache.invalidateQueries();
    fsStore.$reset()
  }
})

const fsStore = useFsStore()
const { removeSelectedPhoto } = fsStore
const selectedPhotos = computed(() =>
  Object.entries(fsStore.selectedPhotos).flatMap(([folder, photos]) =>
    photos.map(photo => ({ folder, photo }))
  )
)
</script>
