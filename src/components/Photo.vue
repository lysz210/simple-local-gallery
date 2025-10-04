<template>
<v-card
flat
class="text-white"
>
    <v-img
    :src="`http://localhost:8000/thumbnails/${currentPhoto.folder}/${currentPhoto.filename}`"
    width="100%"
    >
    <v-toolbar class="text-white" color="transparent">
        <v-toolbar-title>{{ currentPhoto.title }}</v-toolbar-title>
        <ai-helper :photo-id="currentPhoto.id"></ai-helper>
        <flickr-dialog v-if="socialStore.isFlickrActive" :photo="currentPhoto"></flickr-dialog>
    </v-toolbar>
    <v-card-subtitle v-if="currentPhoto.tags">
        <v-chip
        v-for="tag in currentPhoto.tags" :key="tag"
        variant="outlined"
        >{{ tag }}</v-chip>
    </v-card-subtitle>
    <v-card-subtitle class="text-white" v-if="point">
        LAT: {{ point.latitude }} LNG: {{ point.longitude }} TRACK {{ point.track_uid }}
        <span v-if="point.address">{{ point.address.display_name }}</span>
    </v-card-subtitle>
    <v-card-text class="text-white">{{ currentPhoto.description }}</v-card-text>
    </v-img>

    <v-card-actions class="text-black">
        <v-btn v-if="!point"
        v-for="(point, i) in suggetedGpsPoints" :kye="i"
        @click="updatePhotoPoint(point)"
        >{{ point }}</v-btn>
    </v-card-actions>
</v-card>
</template>

<script setup lang="ts">
import AiHelper from './AiHelper.vue';
import FlickrDialog from './FlickrDialog.vue';
import { locatePhotoOnTrackQuery } from '@/slg-api/@pinia/colada/tracks.gen';
import { Photos } from '@/slg-api/sdk.gen';
import type { Photo, PhotoInfo, PointWithTrackUid } from '@/slg-api/types.gen';
import { useSocialStore } from '@/stores/social';
import { useMutation, useQuery } from '@pinia/colada';

const socialStore = useSocialStore();

const { photo } = defineProps<{ photo: Photo }>()

const emit = defineEmits<{
    (e: 'updateGpsPoint', point: PointWithTrackUid): void
}>()

const currentPhoto = ref<Photo>(photo)

const point = ref(photo.point)

const show = ref(false)

const aiInfo = ref<PhotoInfo|null>(null)
const newDescription = ref<string|null>(null)
const selectedAiTags = ref<string[]>([])

const { data: suggetedGpsPoints } = useQuery({
    ...locatePhotoOnTrackQuery({
        query: {
            photo_id: photo.id
        }
    }),
    enabled: !photo.point
})

const { mutate: updatePhotoPoint } = useMutation({
    mutation: async (point: PointWithTrackUid) => {
        const { data } = await Photos.updatePhotoPoint({
            path: { id: photo.id },
            body: point,
            throwOnError: true
        });
        return data;
    },
    onSuccess: (data) => {
        if (data?.point) {
            point.value = data.point
            emit("updateGpsPoint", data.point)
        }
    }
})
</script>
