<template>
<v-container>
<v-row>
    <v-col cols="12">
        <v-autocomplete
            label="Select"
            :items="photosSummaries"
            item-title="folder" item-value="folder"
            v-model="selectedFolder"
            chips closable-chips
        >
            <template v-slot:chip="{ props, item }">
            <v-chip
                v-bind="props"
                :text="`${item.raw.folder} (${item.raw.total_photos})`"
            ></v-chip>
            </template>
        
            <template v-slot:item="{ props, item }">
            <v-list-item
                v-bind="props"
                :subtitle="`${item.raw.first_taken_at} - ${item.raw.last_taken_at}`"
                :title="`${item.raw.folder} with ${item.raw.total_photos}`"
            ></v-list-item>
            </template>
        </v-autocomplete>
    </v-col>
    <v-col v-for="photo in photos" :key="photo.id">
        <Photo
        :photo="photo"
        @gps-point-updated="queryCache.invalidateQueries({ key: [{_id: 'searchPhotos', query: { folder: selectedFolder }}]})"
        ></Photo>
    </v-col>
</v-row>
</v-container>
</template>

<script setup lang="ts">
import Photo from '@/components/Photo.vue'
import { usePhotosInFolder, usePhotosSummaries } from '@/stores/photos'
import { useQueryCache } from '@pinia/colada'

const queryCache = useQueryCache()

const { data: photosSummaries } = usePhotosSummaries()
const { selectedFolder, data: photos } = usePhotosInFolder()

</script>