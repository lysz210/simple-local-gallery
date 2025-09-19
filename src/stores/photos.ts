
import { getPhotosSummaryQuery, searchPhotosQuery, searchPhotosQueryKey } from '@/slg-api/@pinia/colada/photos.gen';
import { Photos } from '@/slg-api/sdk.gen';
import { defineQuery, useQuery } from '@pinia/colada';

export const usePhotosSummaries = defineQuery(() => useQuery({...getPhotosSummaryQuery()}))
export const usePhotosInFolder = defineQuery(() => {
    const selectedFolder = ref(null);
    const queryData = useQuery({
        key: () => searchPhotosQueryKey({ query: { folder: selectedFolder.value }}),
        query: async context => {
                const { data } = await Photos.searchPhotos({
                query: { folder: selectedFolder.value },
                ...context,
                throwOnError: true
            });
            return data;
        },
        enabled: () => !!selectedFolder.value
    })
    return {
        selectedFolder,
        ...queryData
    }
})