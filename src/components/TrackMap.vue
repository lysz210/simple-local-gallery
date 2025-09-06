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
      <l-geo-json :geojson="geoJson" v-if="geoJson"></l-geo-json>
      <l-marker :lat-lng="center"></l-marker>
    </l-map>
  </v-sheet>
</template>

<script setup lang="ts">
import { LGeoJson, LMap, LMarker, LTileLayer } from '@vue-leaflet/vue-leaflet'
import { type FeatureCollection, type Position } from 'geojson'
import { type Track } from '@/slg-api/types.gen'
import { type PointTuple } from 'leaflet';

const attribution=`&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors`
const { gpxData } = defineProps<{ gpxData: Track }>()
const zoom = 15
const center = computed<PointTuple>(() => {
    return (gpxData && gpxData.points)
        ? [gpxData.points[0].latitude, gpxData.points[0].longitude]
        : [45.457753365520205, 12.301083000000004]
})


const geoJson = computed<FeatureCollection>(() => {
  const linePoints: Position[] = gpxData.points?.map(point => [point.longitude, point.latitude]) ?? []
  console.log(linePoints)
  return {
    type: "FeatureCollection",
    features: [{
      type: "Feature",
      geometry: {
          "type": "LineString", 
          "coordinates": linePoints
      },
      properties: {
        name: gpxData.name
      }
    }]
  }
})

</script>