<template>
    <v-card>
        <v-btn
            @click="importPhotos"
            prepend-icon="mdi-tray-arrow-up"
            append-icon="mdi-tray-arrow-up"
            block
        >
            Import Selected Photos
        </v-btn>
        <v-container fluid>
            <v-row>
                <template v-for="(photos, folder) in fsStore.selectedPhotos" :key="folder">
                    <v-col cols="12" v-for="photo in photos" :key="`${photo}`">
                        <v-card>
                            <v-img
                                :src="`http://localhost:8000/static-photos/${photo}`"
                            >
                                <v-card-title class="text-white">{{ photo }}</v-card-title>
                            </v-img>
                        </v-card>
                    </v-col>
                </template>
            </v-row>
        </v-container>
    </v-card>
</template>

<script lang="ts" setup>
import { Photos } from '@/slg-api/sdk.gen';
import { useFsStore } from '@/stores/fs';

const fsStore = useFsStore()

const importPhotos = async () => {
    const selectedPhotos = Object.values(fsStore.selectedPhotos).flat()
    console.log('Importing photos:', selectedPhotos)
    if (selectedPhotos.length === 0) {
        return;
    }
    try {
        const { data: response} = await Photos.importPhotos({
            body: selectedPhotos
        })
        console.log('Import response:', response)
    } catch (error) {
        console.error('Error importing photos:', error)
    }
}
</script>