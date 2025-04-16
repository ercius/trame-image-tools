<script setup lang="ts">
import { computed, defineModel, withDefaults } from "vue";

import type { Vector2D } from "@/types";

interface Props {
  imageSize: Vector2D;
  pixelRatio: number;
  scale: number;
  constrain?: boolean;
  color?: string;
  thickness?: number;
  handleSize?: number;
  handleFillColor?: string;
  handleBorderColor?: string;
  handleBorderSize?: number;
}

type Events = {};

const props = withDefaults(defineProps<Props>(), {
  constrain: true,
  color: "lime",
  thickness: 2,
  handleSize: 10,
  handleFillColor: "#ffffffdd",
  handleBorderColor: "#000000dd",
  handleBorderSize: 1,
});

defineEmits<Events>();

const flatPoints = defineModel<number[]>({ required: true });
const nPoints = computed(() => Math.floor(flatPoints.value.length / 2));
const points = computed(() => {
  const pairs: Vector2D[] = [];
  for (let i = 0; i < nPoints.value; ++i) {
    pairs.push([flatPoints.value[i * 2], flatPoints.value[i * 2 + 1]]);
  }

  return pairs;
});
const pointsStr = computed(() =>
  points.value.map((point) => point.join(",")).join(" "),
);

// Drag widget
function onMouseDownWidget(ev: MouseEvent) {
  ev.stopPropagation();

  let initialPosition = [ev.clientX, ev.clientY];
  const initialPoints = points.value.map((pt) => pt.map((v) => v));

  function onMouseMove(ev: MouseEvent) {
    const dx = initialPosition[0] - ev.clientX;
    const dy = initialPosition[1] - ev.clientY;

    const currPoints = points.value.map((pt) => pt.map((v) => v));

    let newPoints = initialPoints.map(
      (pt) =>
        [
          pt[0] - (props.pixelRatio * dx) / props.scale,
          pt[1] - (props.pixelRatio * dy) / props.scale,
        ] as Vector2D,
    );

    if (props.constrain) {
      newPoints = newPoints.map((pt) => [
        Math.min(Math.max(0, pt[0]), props.imageSize[0]),
        Math.min(Math.max(0, pt[1]), props.imageSize[1]),
      ]);
    }

    newPoints = newPoints.map(
      (pt) => pt.map((val) => Math.round(val)) as Vector2D,
    );

    let changed = false;

    newPoints.forEach((pt, i) => {
      pt.forEach((val, j) => {
        changed = changed || val !== currPoints[i][j];
      });
    });

    if (changed) {
      flatPoints.value = newPoints.flat();
    }
  }

  function onMouseUp() {
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
  }

  document.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseup", onMouseUp);
}

// Drag handle
function onMouseDownHandle(idx: number, ev: MouseEvent) {
  ev.stopPropagation();

  let initialPosition = [ev.clientX, ev.clientY];
  const initialPoints = points.value.map((pt) => pt.map((v) => v));

  function onMouseMove(ev: MouseEvent) {
    const dx = initialPosition[0] - ev.clientX;
    const dy = initialPosition[1] - ev.clientY;

    const currPoints = points.value.map((pt) => pt.map((v) => v)) as Vector2D[];

    let newPoints = points.value.map((pt) => pt.map((v) => v)) as Vector2D[];

    newPoints[idx] = [
      initialPoints[idx][0] - (props.pixelRatio * dx) / props.scale,
      initialPoints[idx][1] - (props.pixelRatio * dy) / props.scale,
    ];

    if (props.constrain) {
      newPoints[idx][0] = Math.min(
        Math.max(0, newPoints[idx][0]),
        props.imageSize[0],
      );
      newPoints[idx][1] = Math.min(
        Math.max(0, newPoints[idx][1]),
        props.imageSize[1],
      );
    }

    newPoints = newPoints.map(
      (pt) => pt.map((val) => Math.round(val)) as Vector2D,
    );

    let changed =
      newPoints[idx][0] !== currPoints[idx][0] ||
      newPoints[idx][1] !== currPoints[idx][1];

    if (changed) {
      flatPoints.value = newPoints.flat();
    }
  }

  function onMouseUp() {
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
  }

  document.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseup", onMouseUp);
}
</script>

<template>
  <g>
    <polyline
      @mousedown="onMouseDownWidget"
      :points="pointsStr"
      :stroke="color"
      :stroke-width="(thickness * pixelRatio) / scale"
      fill="none"
    />

    <rect
      v-for="(point, i) in points"
      :key="i"
      @mousedown="(ev: MouseEvent) => onMouseDownHandle(i, ev)"
      :x="point[0] - (0.5 * handleSize * pixelRatio) / scale"
      :y="point[1] - (0.5 * handleSize * pixelRatio) / scale"
      :width="(handleSize * pixelRatio) / scale"
      :height="(handleSize * pixelRatio) / scale"
      :stroke="handleBorderColor"
      :fill="handleFillColor"
      :stroke-width="pixelRatio / scale"
    />
  </g>
</template>
