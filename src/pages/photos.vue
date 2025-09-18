<template>
<v-container>
    <v-row><v-col cols="12">
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
    </v-col></v-row>
</v-container>
</template>

<script setup lang="ts">
import { usePhotosSummaries } from '@/stores/photos'

const selectedFolder = ref(null)
const { data: photosSummaries } = usePhotosSummaries()
</script>