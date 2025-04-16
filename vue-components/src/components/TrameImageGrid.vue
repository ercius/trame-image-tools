<script setup lang="ts">
import { withDefaults, computed } from "vue";

import type { Vector2D } from "@/types";

interface Props {
  imageSize: Vector2D;
  pixelRatio: number;
  scale: number;
  spacing: Vector2D;
  color?: string;
  thickness?: number;
  fontFamily?: string;
  fontSize?: number;
}

type Events = {};

const props = withDefaults(defineProps<Props>(), {
  color: "#ffffffaa",
  thickness: 0.5,
  fontFamily: "monospace",
  fontSize: 12,
});

defineEmits<Events>();

const xTicks = computed(() => {
  const ticks = [];
  const nTicks = Math.floor(props.imageSize[0] / props.spacing[0]) + 1;
  for (let i = 0; i < nTicks; ++i) {
    ticks.push(i * props.spacing[0]);
  }

  return ticks;
});

const yTicks = computed(() => {
  const ticks = [];
  const nTicks = Math.floor(props.imageSize[1] / props.spacing[1]) + 1;
  for (let i = 0; i < nTicks; ++i) {
    ticks.push(i * props.spacing[1]);
  }

  return ticks;
});
</script>

<template>
  <g>
    <template v-for="(x, i) in xTicks" :key="i">
      <line
        :x1="x"
        :y1="0"
        :x2="x"
        :y2="props.imageSize[1]"
        :stroke="color"
        :stroke-width="(thickness * pixelRatio) / scale"
        pointer-events="none"
      />

      <text
        :x="x"
        :y="(-fontSize * pixelRatio) / scale"
        :fill="color"
        :font-family="fontFamily"
        text-anchor="middle"
        :font-size="(fontSize * pixelRatio) / scale"
        pointer-events="none"
        style="user-select: none"
      >
        {{ x }}
      </text>
    </template>

    <template v-for="(y, i) in yTicks" :key="i">
      <line
        :x1="0"
        :y1="y"
        :x2="props.imageSize[0]"
        :y2="y"
        :stroke="color"
        :stroke-width="(thickness * pixelRatio) / scale"
        pointer-events="none"
      />

      <text
        :x="(-fontSize * pixelRatio) / scale"
        :y="y"
        :fill="color"
        :font-family="fontFamily"
        text-anchor="end"
        dominant-baseline="middle"
        :font-size="(fontSize * pixelRatio) / scale"
        pointer-events="none"
        style="user-select: none"
      >
        {{ y }}
      </text>
    </template>
  </g>
</template>
