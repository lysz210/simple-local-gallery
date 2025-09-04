<template>
    <v-container>
        <v-list>
            <v-list-item
            v-for="photo in photos.data" :key="photo"
            :title="`${photo}`"
            ></v-list-item>
        </v-list>
    </v-container>
</template>
<script lang="ts" setup>
import { findPhotosQueryKey } from '@/slg-api/@pinia/colada/filesystem.gen';
import { Filesystem, type Options } from '@/slg-api/sdk.gen';
import type { FindPhotosData } from '@/slg-api/types.gen';
import { defineQueryOptions, useQuery } from '@pinia/colada';

const route = useRoute()

const { state: photos } = useQuery(
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
</script>