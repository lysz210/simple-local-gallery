<template>
<v-container>
    <v-row>
        <v-col
        v-for="photo in photos" :key="photo"
        class="d-flex child-flex"
        cols="4"
        >
        <v-img
            :src="`http://localhost:8000/static-photos/${photo}`"
            aspect-ratio="1"
            class="bg-grey-lighten-2"
            cover
        >
            <template v-slot:placeholder>
            <v-row
                align="center"
                class="fill-height ma-0"
                justify="center"
            >
                <v-progress-circular
                color="grey-lighten-5"
                indeterminate
                ></v-progress-circular>
            </v-row>
            </template>
        </v-img>
        </v-col>
    </v-row>
</v-container>
</template>
<script lang="ts" setup>
import { findPhotosQueryKey } from '@/slg-api/@pinia/colada/filesystem.gen';
import { Filesystem, type Options } from '@/slg-api/sdk.gen';
import type { FindPhotosData } from '@/slg-api/types.gen';
import { defineQueryOptions, useQuery } from '@pinia/colada';

const route = useRoute()
const router = useRouter()

const { data: photos, error: photosError } = useQuery(
    defineQueryOptions((folder: string) => {
        const options: Options<FindPhotosData> = {
            path: {
                folder
            }
        }
        return {
            key: findPhotosQueryKey(options),
            query: async (context) => {
                const { data } = await Filesystem.findPhotos({
                    ...options,
                    ...context,
                    throwOnError: true
                })
                return data
            }
        }
    }),
    () => route.params.folder.join('/')
)

watch(photosError, async (newError) => {
    if (newError) {
        console.error(newError)
        router.push("/")
    }
})
</script>