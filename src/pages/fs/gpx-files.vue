<template>
    <v-container>
        <v-autocomplete
            label="Select"
            :items="gpxFiles.data"
            v-model="selectedGpxFile"
        ></v-autocomplete>
        <v-btn
            v-if="selectedGpxFile"
            @click="importGpx(selectedGpxFile)"
            prepend-icon="mdi-tray-arrow-up"
            append-icon="mdi-tray-arrow-up"
            block
        >
            Import {{ gpxData?.uid }}  {{ gpxData?.name }} - {{ gpxData?.timestamp }} with {{ gpxData?.points?.length }} points
        </v-btn>
        <TrackMap :gpxData="gpxData" v-if="!gpxError && gpxData"></TrackMap>
    </v-container>
</template>

<script lang="ts" setup>
import TrackMap from '@/components/TrackMap.vue';
import { findGpxFilesQuery } from '@/slg-api/@pinia/colada/filesystem.gen';
import { inspectGpxFileQueryKey } from '@/slg-api/@pinia/colada/tracks.gen';
import { Tracks, type Options } from '@/slg-api/sdk.gen';
import type { InspectGpxFileData } from '@/slg-api/types.gen';
import { defineQueryOptions, useQuery, useQueryCache } from '@pinia/colada';

const router = useRouter()
const queryCache = useQueryCache()

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

async function importGpx(gpxFile: string) {
    try {
        const { data: trackUid } = await Tracks.importPgxFile({
            path: {
                gpx_file: gpxFile
            }
        });
        console.info("Imported gpxFile", trackUid)
        queryCache.invalidateQueries({
            key: [{tags: ["tracks"]}]
        })
    } catch (error) {
        console.error("Error importing gpxFile", gpxFile, error);
    }
}

watch(gpxError, async (newError) => {
    if (newError) {
        console.error(newError)
        router.push("/")
    }
})
</script>