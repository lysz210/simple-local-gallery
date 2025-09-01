<template>
<v-navigation-drawer app>
    <v-list nav>
      <v-list-item
      v-for="summary in photosSummaries" :key="summary.folder"
      :title="`${summary.folder} with ${summary.total_photos} photos`"
      ></v-list-item>
    </v-list>

    <v-list nav>
      <v-list-item
      v-for="summary in tracksSummaries" :key="summary.uid"
      :title="`${summary.uid} ${summary.name} with ${summary.total_points} points`"
      ></v-list-item>
    </v-list>
</v-navigation-drawer>
</template>

<script lang="ts" setup>
import { Photos, Tracks, type PhotoSummary, type TrackSummary } from '@/slg-api';

const photosSummaries: Ref<PhotoSummary[]> = ref([])
const tracksSummaries: Ref<TrackSummary[]> = ref([])

Photos.getPhotosSummary().then(res => {
  photosSummaries.value = res?.data ?? []
})

Tracks.getTracksSummary().then(res => {
  tracksSummaries.value = res?.data ?? []
})
</script>
