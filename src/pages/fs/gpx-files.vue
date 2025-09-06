<template>
    <v-container>
        <v-autocomplete
            label="Select"
            :items="gpxFiles.data"
            v-model="selectedGpxFile"
        ></v-autocomplete>
        <p>{{ gpxData?.uid }}  {{ gpxData?.name }}</p>
        <p>{{ gpxData?.timestamp }}</p>
        <p>{{ gpxData?.points?.length }}</p>
        <TrackMap :gpxData="gpxData" v-if="!gpxError && gpxData"></TrackMap>
    </v-container>
</template>

<script lang="ts" setup>
import TrackMap from '@/components/TrackMap.vue';
import { findGpxFilesQuery } from '@/slg-api/@pinia/colada/filesystem.gen';
import { inspectGpxFileQueryKey } from '@/slg-api/@pinia/colada/tracks.gen';
import { Tracks, type Options } from '@/slg-api/sdk.gen';
import type { InspectGpxFileData } from '@/slg-api/types.gen';
import { defineQueryOptions, useQuery } from '@pinia/colada';

const router = useRouter()

const selectedGpxFile = ref(null)

const { state: gpxFiles } = useQuery({...findGpxFilesQuery()})

const gpxInpectQuery = defineQueryOptions((gpx_file: string|null) => {

    const options: Options<InspectGpxFileData> = {
        path: {
            gpx_file: gpx_file ?? ''
        }
    }

    return {
        key: inspectGpxFileQueryKey(options),
        query: async (context) => {
            if (gpx_file === null) {
                return null
            }
            const { data } = await Tracks.inspectGpxFile({
                ...options,
                ...context,
                throwOnError: true
            });
            return data;
        }
    };
})

const { data: gpxData, error: gpxError } = useQuery(gpxInpectQuery, () => selectedGpxFile.value)
watch(gpxError, async (newError) => {
    if (newError) {
        console.error(newError)
        router.push("/")
    }
})
</script>