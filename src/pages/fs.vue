<template>
  <v-card width="100%">
    <v-tabs
      v-model="tab"
      bg-color="primary"
      fixed-tabs
    >
    <v-tab :value="PHOTOS_TAB">Photos folder</v-tab>
    <v-tab :value="SELECTED_PHOTOS_TAB">Selected Photos</v-tab>
    <v-tab :value="GPX_TAB">Gpx files</v-tab>
    </v-tabs>

    <v-card-text>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item :value="GPX_TAB">
          <FsTracks></FsTracks>
        </v-tabs-window-item>

        <v-tabs-window-item :value="PHOTOS_TAB">
          <FsPhotos></FsPhotos>
        </v-tabs-window-item>

        <v-tabs-window-item :value="SELECTED_PHOTOS_TAB">
          <FsSelectedPhotos></FsSelectedPhotos>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { useFsStore } from '@/stores/fs'

const GPX_TAB = 'gpx'
const PHOTOS_TAB = 'photos'
const SELECTED_PHOTOS_TAB = 'selected_photos'
const tab = ref(PHOTOS_TAB)

const fsStore = useFsStore()

watch(tab, (newTab) => {
  fsStore.previewSelecetedPhotos = newTab === PHOTOS_TAB
})

onUnmounted(() => {
  fsStore.previewSelecetedPhotos = false
})
</script>