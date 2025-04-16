<script setup lang="ts">
import { defineModel, withDefaults } from "vue";

import type { Vector2D, Vector3D } from "@/types";

interface Props {
  imageSize: Vector2D;
  pixelRatio: number;
  scale: number;
  constrain?: boolean;
  fillColor?: string;
  borderColor?: string;
  borderSize?: number;
  handleSize?: number;
  handleFillColor?: string;
  handleBorderColor?: string;
}

type Events = {};

const props = withDefaults(defineProps<Props>(), {
  constrain: true,
  fillColor: "transparent",
  borderColor: "lime",
  borderSize: 2,
  handleSize: 10,
  handleFillColor: "#ffffffdd",
  handleBorderColor: "#000000dd",
});

defineEmits<Events>();

const circle = defineModel<Vector3D>({ required: true });

// Drag widget
function onMouseDownWidget(ev: MouseEvent) {
  ev.stopPropagation();

  let initialPosition = [ev.clientX, ev.clientY];
  const initialCircle: Vector3D = [...circle.value];

  function onMouseMove(ev: MouseEvent) {
    const dx = initialPosition[0] - ev.clientX;
    const dy = initialPosition[1] - ev.clientY;

    const currCircle: Vector3D = [...circle.value];

    let newCircle: Vector3D = [
      initialCircle[0] - (props.pixelRatio * dx) / props.scale,
      initialCircle[1] - (props.pixelRatio * dy) / props.scale,
      currCircle[2],
    ];

    if (props.constrain) {
      newCircle[0] = Math.min(Math.max(0, newCircle[0]), props.imageSize[0]);
      newCircle[1] = Math.min(Math.max(0, newCircle[1]), props.imageSize[1]);
    }

    newCircle = newCircle.map((val) => Math.round(val)) as Vector3D;

    let changed = false;

    newCircle.forEach((val, i) => {
      changed = changed || val !== currCircle[i];
    });

    if (changed) {
      circle.value = newCircle;
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
  const initialCircle: Vector3D = [...circle.value];

  function onMouseMove(ev: MouseEvent) {
    const dx = initialPosition[0] - ev.clientX;

    const currCircle: Vector3D = [...circle.value];

    let newCircle: Vector3D = [
      currCircle[0],
      currCircle[1],
      initialCircle[2] - (props.pixelRatio * dx) / props.scale,
    ];

    newCircle[2] = Math.max(1, newCircle[2]);

    newCircle = newCircle.map((val) => Math.round(val)) as Vector3D;

    let changed = false;

    newCircle.forEach((val, i) => {
      changed = changed || val !== currCircle[i];
    });

    if (changed) {
      circle.value = newCircle;
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
    <circle
      @mousedown="onMouseDownWidget"
      :cx="circle[0]"
      :cy="circle[1]"
      :r="circle[2]"
      :stroke="borderColor"
      :fill="fillColor"
      :stroke-width="(borderSize * pixelRatio) / scale"
    />

    <circle
      :cx="circle[0]"
      :cy="circle[1]"
      :r="(0.5 * pixelRatio) / scale"
      :stroke="borderColor"
      :stroke-width="(borderSize * pixelRatio) / scale"
      fill="transparent"
    />

    <rect
      @mousedown="(ev: MouseEvent) => onMouseDownHandle(0, ev)"
      :x="circle[0] + circle[2] - (0.5 * handleSize * pixelRatio) / scale"
      :y="circle[1] - (0.5 * handleSize * pixelRatio) / scale"
      :width="(handleSize * pixelRatio) / scale"
      :height="(handleSize * pixelRatio) / scale"
      :stroke="handleBorderColor"
      :fill="handleFillColor"
      :stroke-width="pixelRatio / scale"
    />
  </g>
</template>
