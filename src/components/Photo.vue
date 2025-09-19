<template>
<v-card
flat
>
    <v-img
    :src="`http://localhost:8000/thumbnails/${photo.folder}/${photo.filename}`"
    width="100%"
    >
    <v-card-title class="text-white">{{ photo.description }}</v-card-title>
    <v-card-subtitle class="text-white" v-if="point">
        LAT: {{ point.latitude }} LNG: {{ point.longitude }}
    </v-card-subtitle>
    </v-img>

    <v-card-actions v-if="!point">
        <v-btn
        v-for="(point, i) in suggetedGpsPoints" :kye="i"
        @click="updatePhotoPoint(point)"
        >{{ point }}</v-btn>
    </v-card-actions>
</v-card>
</template>

<script setup lang="ts">
import { locatePhotoOnTrackQuery } from '@/slg-api/@pinia/colada/tracks.gen';
import { Photos } from '@/slg-api/sdk.gen';
import type { Photo, PointWithTrackUid } from '@/slg-api/types.gen';
import { useMutation, useQuery } from '@pinia/colada';

const { photo } = defineProps<{ photo: Photo }>()

const emit = defineEmits(["gpsPointUpdated"])

const point = computed(() => photo.point)

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
        emit("gpsPointUpdated")
    }
})

</script>
