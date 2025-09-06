<template>
  <v-sheet width="100%" height="600px">

    <l-map ref="map" v-model:zoom="zoom" :center="[45.457753365520205, 12.301083000000004]">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
        :attribution="attribution"
      ></l-tile-layer>
    </l-map>
  </v-sheet>
</template>

<script lang="ts" setup>
import { LMap, LTileLayer } from '@vue-leaflet/vue-leaflet'

const zoom = 6
const attribution=`&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors`
</script>
