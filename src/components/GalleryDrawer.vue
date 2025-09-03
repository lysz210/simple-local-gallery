<template>
<v-navigation-drawer app>
    <v-list nav>
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

      <v-list-group value="Filesystem Summaries" v-if="!fsSummaries.error">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            title="Filesystem Summaries"
            prepend-icon="mdi-file-tree"
          ></v-list-item>
        </template>
        <v-list-item
          v-if="fsSummaries.data?.gpx_files_count"
          :title="`Found ${fsSummaries.data.gpx_files_count} GPX files`"
          link to="/fs/gpx-files"
        ></v-list-item>
        <v-list-item
          v-for="summary in fsSummaries.data?.folders" :key="summary.folder"
          :title="`${summary.folder}`"
          :subtitle="`with ${summary.total_photos} photos`"
        ></v-list-item>
      </v-list-group>
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
