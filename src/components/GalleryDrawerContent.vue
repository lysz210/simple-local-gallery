<template>
  <v-list nav>
    <v-list-item
      title="Filesystem Summaries"
      prepend-icon="mdi-home"
      link to="/"
    ></v-list-item>
    
    <v-list-group value="Photos Summaries" v-if="!photosSummaries.error">
      <template v-slot:activator="{ props }">
        <v-list-item
          v-bind="props"
          title="Photos Summaries"
          prepend-icon="mdi-image-album"
        ></v-list-item>
      </template>
      <v-list-item
        v-for="summary in photosSummaries.data" :key="summary.folder"
        :title="`${summary.folder}`"
        :subtitle="`with ${summary.total_photos} photos`"
      ></v-list-item>
    </v-list-group>

    <v-list-group value="Tracks Summaries" v-if="!tracksSummaries.error">
      <template v-slot:activator="{ props }">
        <v-list-item
          v-bind="props"
          title="Tracks Summaries"
          prepend-icon="mdi-map-marker-path"
        ></v-list-item>
      </template>
      <v-list-item
        v-for="summary in tracksSummaries.data" :key="summary.uid"
        :title="`track[${summary.uid}] with ${summary.total_points} points`"
        :subtitle="`${summary.name}`"
      ></v-list-item>
    </v-list-group>

    <v-list-item
      title="Filesystem Summaries"
      prepend-icon="mdi-file-tree"
      link to="/fs"
    ></v-list-item>
  </v-list>

  <v-container v-for="(photos, folder) in fsStore.selectedPhotos" :key="folder">
    <v-row><v-col>
      <v-img
        v-for="photo in photos" :key="photo"
        :src="`http://localhost:8000/static-photos/${photo}`"
        @click="removeSelectedPhoto(folder, photo)"
      ></v-img>
    </v-col></v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { getPhotosSummaryQuery } from '@/slg-api/@pinia/colada/photos.gen';
import { useFsStore } from '@/stores/fs';
import { useTraksSummaries } from '@/stores/traks';
import { useQuery } from '@pinia/colada';

const { state: photosSummaries } = useQuery({...getPhotosSummaryQuery()})
const { state: tracksSummaries } = useTraksSummaries()
const fsStore = useFsStore()
const { removeSelectedPhoto } = fsStore
</script>
