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
    </v-card-subtitle>
    <v-card-text class="text-white">{{ currentPhoto.description }}</v-card-text>
    </v-img>

    <v-card-actions>
        <v-btn v-if="!point"
        v-for="(point, i) in suggetedGpsPoints" :kye="i"
        @click="updatePhotoPoint(point)"
        >{{ point }}</v-btn>
        <v-btn v-if="!aiInfo"
        @click="inspectPhoto(photo)"
        >Inspect photo with AI</v-btn>
        
    </v-card-actions>
    <v-expand-transition>
        <v-card-text v-if="aiInfo"
        >
        <v-textarea
        label="Ai description"
        v-model="newDescription"
        ></v-textarea>
        
        <v-chip-group
        v-model="selectedAiTags"
        multiple column
        >
            <v-chip v-for="tag in aiInfo.tags" :value="tag" filter>{{ tag }}</v-chip>
        </v-chip-group>
        {{ selectedAiTags }}
        <v-btn @click="patchPhoto({ description: newDescription, tags: selectedAiTags })">Update photo infos</v-btn>
        </v-card-text>
    </v-expand-transition>
</v-card>
</template>

<script setup lang="ts">
import AiHelper from './AiHelper.vue';
import FlickrDialog from './FlickrDialog.vue';
import { locatePhotoOnTrackQuery } from '@/slg-api/@pinia/colada/tracks.gen';
import { Ai, Photos } from '@/slg-api/sdk.gen';
import type { Photo, PhotoInfo, PhotoPatch, PointWithTrackUid } from '@/slg-api/types.gen';
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

const { mutate: inspectPhoto } = useMutation({
    mutation: async (photo: Photo) => {
        const { data } = await Ai.inpectPhoto({
            query: { id: photo.id },
            throwOnError: true
        });
        return data;
    },
    onSuccess: (data) => {
        aiInfo.value = data;
        newDescription.value = data.description;
        selectedAiTags.value.push(...data.tags);
    }
})

const { mutate: patchPhoto } = useMutation({
    mutation: async (body: PhotoPatch) => {
        const { data } = await Photos.patchPhoto({
            path: { id: photo.id },
            body,
            throwOnError: true
        });
        return data;
    },
    onSuccess: (data) => {
        currentPhoto.value = data;
        aiInfo.value = null;
        selectedAiTags.value = [];
        newDescription.value = null;
    }
})
</script>
