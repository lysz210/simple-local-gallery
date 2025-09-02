<template>
<v-navigation-drawer app>
    <v-list nav v-if="!photosSummaries.error">
      <v-list-item
      v-for="summary in photosSummaries.data" :key="summary.folder"
      :title="`${summary.folder} with ${summary.total_photos} photos`"
      ></v-list-item>
    </v-list>

    <v-list nav v-if="!tracksSummaries.error">
      <v-list-item
      v-for="summary in tracksSummaries.data" :key="summary.uid"
      :title="`${summary.uid} ${summary.name} with ${summary.total_points} points`"
      ></v-list-item>
    </v-list>

    <v-list nav v-if="!fsSummaries.error">
      <v-list-item v-if="fsSummaries.data?.gpx_files_count"
      :title="`Found ${fsSummaries.data.gpx_files_count} GPX files`"
      ></v-list-item>
      <v-list-item
      v-for="summary in fsSummaries.data?.folders" :key="summary.folder"
      :title="`${summary.folder} with ${summary.total_photos} photos`"
      ></v-list-item>
    </v-list>
</v-navigation-drawer>
</template>

<script lang="ts" setup>
import { getFilesystemSummaryQuery } from '@/slg-api/@pinia/colada/filesystem.gen';
import { getPhotosSummaryQuery } from '@/slg-api/@pinia/colada/photos.gen';
import { getTracksSummaryQuery } from '@/slg-api/@pinia/colada/tracks.gen';
import { useQuery } from '@pinia/colada';

const { state: photosSummaries } = useQuery({...getPhotosSummaryQuery()})
const { state: tracksSummaries } = useQuery({...getTracksSummaryQuery()})
const { state: fsSummaries } = useQuery({...getFilesystemSummaryQuery()})
</script>
