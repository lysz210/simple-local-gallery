<template>
  <v-sheet width="100%" height="600px">

    <l-map ref="map" v-model:zoom="zoom" :center="[45.457753365520205, 12.301083000000004]">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
        :attribution="attribution"
      ></l-tile-layer>
      <l-rectangle
        v-for="(bounds, index) in trackBounds" :key="index"
        :bounds="[[bounds.min.latitude, bounds.min.longitude], [bounds.max.latitude, bounds.max.longitude]]"
        color="blue"
      ></l-rectangle>
    </l-map>
  </v-sheet>
</template>

<script lang="ts" setup>
import { useTraksSummaries } from '@/stores/traks'
import { latLng, latLngBounds } from 'leaflet'
import { LMap, LTileLayer, LRectangle } from '@vue-leaflet/vue-leaflet'

const zoom = 6
const attribution=`&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors`

const mapRef = useTemplateRef('map')
const { data: tracksSummaries } = useTraksSummaries()

const trackBounds = computed(() => {
  if (!tracksSummaries.value?.length) {
    return []
  }
  return tracksSummaries.value
    .map(track => track.bounds)
    .filter(bounds => !!bounds)
})

watchEffect(() => {
  if (tracksSummaries.value?.length) {
    const boundsValues = tracksSummaries.value
      .map(track => track.bounds)
      .filter(bounds => !!bounds)
      .reduce((acc, bounds) => {
        acc.minLat.push(bounds.min.latitude);
        acc.minLng.push(bounds.min.longitude);
        acc.maxLat.push(bounds.max.latitude);
        acc.maxLng.push(bounds.max.longitude);
        return acc;
      }, {
        minLat: [] as number[],
        minLng: [] as number[],
        maxLat: [] as number[],
        maxLng: [] as number[]
      })
    if (boundsValues.minLat && boundsValues.minLng && boundsValues.maxLat && boundsValues.maxLng) {
      const bounds = latLngBounds(
        latLng(Math.min(...boundsValues.minLat), Math.min(...boundsValues.minLng)),
        latLng(Math.max(...boundsValues.maxLat), Math.max(...boundsValues.maxLng))
      )
      // @ts-ignore
      mapRef.value?.leafletObject.fitBounds(bounds);
    }
  }
})
</script>
