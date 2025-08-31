<template>
  <HelloWorld />
</template>

<script lang="ts" setup>
import { Photos } from '@/slg-api/sdk.gen'

const { data } = await Photos.getApiV1Photos()
console.log(data)
</script>
