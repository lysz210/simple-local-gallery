<template>
    <v-container>
        <v-autocomplete
            label="Select"
            :items="gpxFiles.data"
            v-model="selectedGpxFile"
        ></v-autocomplete>
        <p>{{ selectedGpxFile }}</p>
        <p>{{ gpxData.data?.uid }}  {{ gpxData.data?.name }}</p>
        <p>{{ gpxData.data?.timestamp }}</p>
        <p>{{ gpxData.data?.points?.length }}</p>
    </v-container>
</template>

<script lang="ts" setup>
import { findGpxFilesQuery } from '@/slg-api/@pinia/colada/filesystem.gen';
import { getTracksSummaryQueryKey, inspectPgxFileQuery, inspectPgxFileQueryKey } from '@/slg-api/@pinia/colada/tracks.gen';
import { Tracks, type Options } from '@/slg-api/sdk.gen';
import type { InspectPgxFileData } from '@/slg-api/types.gen';
import { defineQueryOptions, useQuery } from '@pinia/colada';

const selectedGpxFile = ref(null)

const { state: gpxFiles } = useQuery({...findGpxFilesQuery()})

const gpxInfoEnabled = computed(() => {
    return selectedGpxFile.value !== null
});

const gpxInpectQuery = defineQueryOptions((gpx_file: string|null) => {

    const options: Options<InspectPgxFileData> = {
        path: {
            gpx_file: gpx_file ?? ''
        }
    }

    return {
        key: inspectPgxFileQueryKey(options),
        query: async (context) => {
            if (gpx_file === null) {
                return null
            }
            const { data } = await Tracks.inspectPgxFile({
                ...options,
                ...context,
                throwOnError: true
            });
            return data;
        }
    };
})

const { state: gpxData } = useQuery(gpxInpectQuery, () => selectedGpxFile.value)
</script>