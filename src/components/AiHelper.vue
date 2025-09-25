<template>
    <v-dialog v-model="isOpened">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn color="transparent" v-bind="activatorProps" variant="flat" icon="mdi-robot"></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card title="Ai Generated contents" :loading="isLoading">
                <v-card-title>{{ photoInfo?.title }}</v-card-title>
                <v-card-text>{{ photoInfo?.description }}</v-card-text>
                <v-card-text>
                    <v-autocomplete
                        label="Tags"
                        :items="photoInfo.tags"
                        v-model="tags"
                        v-if="photoInfo?.tags"
                        multiple chips closable-chips
                    ></v-autocomplete>
                    {{ photoInfo?.tags }}
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="() => patchPhoto()">Update Photo info</v-btn>
                    <v-btn text="Close Dialog" @click="isActive.value = false"></v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script setup lang="ts">
import { inpectPhotoQuery } from '@/slg-api/@pinia/colada/ai.gen';
import { Photos } from '@/slg-api/sdk.gen';
import { useMutation, useQuery } from '@pinia/colada';

const { photoId } = defineProps<{
    photoId: number
}>()

const isOpened = ref(false)
const tags = ref<string[]>([])

const { data: photoInfo, isLoading } = useQuery({
    ...inpectPhotoQuery({
        query: {
            id: photoId
        }
    }),
    staleTime: 3600,
    enabled: isOpened,
})

const { mutate: patchPhoto } = useMutation({
    mutation: async () => {
        const { data } = await Photos.patchPhoto({
            path: { id: photoId },
            body: {
                title: photoInfo.value?.title,
                description: photoInfo.value?.description,
                tags: tags.value
            }
        });
        return data;
    },
    onSettled: async () => {
        isOpened.value = false
    }
})

watchEffect(() => {
    if (photoInfo.value?.tags) {
        tags.value = [...photoInfo.value.tags]
    }
})

</script>