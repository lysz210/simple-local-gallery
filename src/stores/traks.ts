import { getTracksSummaryQuery } from "@/slg-api/@pinia/colada/tracks.gen";
import { defineQuery, useQuery } from "@pinia/colada";

export const useTraksSummaries = defineQuery(() => useQuery(getTracksSummaryQuery()))