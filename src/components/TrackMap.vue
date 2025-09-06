<template>
  <v-sheet width="100%" height="600px">
    <l-map ref="map" v-model:zoom="zoom" :center="center">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
        :no-wrap="true"
        :attribution="attribution"
      ></l-tile-layer>
    </l-map>
  </v-sheet>
</template>

<script setup lang="ts">
import { LMap, LTileLayer } from '@vue-leaflet/vue-leaflet'
import { type Track } from '@/slg-api/types.gen'
import { type PointExpression } from 'leaflet';

const { gpxData } = defineProps<{ gpxData: Track }>()
const zoom = 10
const center = computed<PointExpression>(() => {
    return (gpxData && gpxData.points)
        ? [gpxData.points[0].latitude, gpxData.points[0].longitude]
        : [47.41322, -1.219482]
})
const attribution=`&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors`
</script>