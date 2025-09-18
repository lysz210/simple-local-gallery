<template>
  <v-list nav>
    <v-list-item
      title="Filesystem Summaries"
      prepend-icon="mdi-home"
      link to="/"
    ></v-list-item>
    
    <v-list-item
      title="Photos"
      prepend-icon="mdi-image-album"
      link to="/photos"
    ></v-list-item>

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
</template>

<script lang="ts" setup>
import { useTraksSummaries } from '@/stores/traks';

const { state: tracksSummaries } = useTraksSummaries()
</script>
