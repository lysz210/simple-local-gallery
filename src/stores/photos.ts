
import { getPhotosSummaryQuery } from '@/slg-api/@pinia/colada/photos.gen';
import { defineQuery, useQuery } from '@pinia/colada';

export const usePhotosSummaries = defineQuery(() => useQuery({...getPhotosSummaryQuery()}))