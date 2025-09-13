<template>
  <v-card width="100%">
    <v-tabs
      v-model="tab"
      bg-color="primary"
      fixed-tabs
    >
      <v-tab :value="GPX_TAB">Gpx files</v-tab>
      <v-tab :value="PHOTOS_TAB">Photos folder</v-tab>
    </v-tabs>

    <v-card-text>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item :value="GPX_TAB">
          <FsTracks></FsTracks>
        </v-tabs-window-item>

        <v-tabs-window-item :value="PHOTOS_TAB">
          <FsPhotos></FsPhotos>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
const GPX_TAB = 'gpx'
const PHOTOS_TAB = 'photos'
const tab = ref(GPX_TAB)
</script>