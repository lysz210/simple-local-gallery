<template>
    <v-dialog v-model="isOpened">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn color="transparent" v-bind="activatorProps" variant="flat" icon="mdi-share-variant"></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card title="Flickr photo" :loading="isLoading">
                <v-card-title>{{ info?.title }}</v-card-title>
                <v-card-title>{{ photo.title }}</v-card-title>
                <v-card-text>{{ info?.description }}</v-card-text>
                <v-card-text>{{ photo.description }}</v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="() => updateFlickrPhoto()">Update Photo info</v-btn>
                    <v-btn text="Close Dialog" @click="isActive.value = false"></v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script setup lang="ts">
import { photoInfoQuery } from '@/slg-api/@pinia/colada/flickr.gen';
import { Flickr } from '@/slg-api/sdk.gen';
import type { Photo } from '@/slg-api/types.gen';
import { useMutation, useQuery } from '@pinia/colada';

const { photo } = defineProps<{
    photo: Photo
}>()

const isOpened = ref(false)
const photoId = computed(() => photo.id)

const { data: info, isLoading } = useQuery({
    ...photoInfoQuery({
        query: { id: photo.id }
    }),
    enabled: isOpened
})

const { mutate: updateFlickrPhoto } = useMutation({
    mutation: async () => {
        const { data } = await Flickr.updatePhotoInfo({
            query: { id: photo.id }
        });
        return data;
    },
    onSettled: async () => {
        isOpened.value = false;
    }
})
</script>