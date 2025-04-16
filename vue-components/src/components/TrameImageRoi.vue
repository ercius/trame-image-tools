<script setup lang="ts">
import { defineModel, withDefaults } from "vue";

import type { Vector2D, ViewBox } from "@/types";

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

const roi = defineModel<ViewBox>({ required: true });

// Drag widget
function onMouseDownWidget(ev: MouseEvent) {
  ev.stopPropagation();

  let initialPosition = [ev.clientX, ev.clientY];
  const initialRoi: ViewBox = [...roi.value];

  const imageWidth = props.imageSize[0];
  const imageHeight = props.imageSize[1];

  function onMouseMove(ev: MouseEvent) {
    const dx = initialPosition[0] - ev.clientX;
    const dy = initialPosition[1] - ev.clientY;

    const currRoi: ViewBox = [...roi.value];

    let newRoi: ViewBox = [
      initialRoi[0] - (props.pixelRatio * dx) / props.scale,
      initialRoi[1] - (props.pixelRatio * dy) / props.scale,
      currRoi[2],
      currRoi[3],
    ];

    if (props.constrain) {
      if (newRoi[0] < 0) {
        newRoi[0] = 0;
      }

      if (newRoi[1] < 0) {
        newRoi[1] = 0;
      }

      if (newRoi[0] + currRoi[2] > imageWidth) {
        newRoi[0] = imageWidth - currRoi[2];
      }

      if (newRoi[1] + currRoi[3] > imageHeight) {
        newRoi[1] = imageHeight - currRoi[3];
      }
    }

    newRoi = newRoi.map((val) => Math.round(val)) as ViewBox;

    let changed = false;

    newRoi.forEach((val, i) => {
      changed = changed || val !== currRoi[i];
    });

    if (changed) {
      roi.value = newRoi;
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
function onMouseDownHandle(ev: MouseEvent) {
  ev.stopPropagation();

  let initialPosition = [ev.clientX, ev.clientY];
  const initialRoi: ViewBox = [...roi.value];

  const imageWidth = props.imageSize[0];
  const imageHeight = props.imageSize[1];

  function onMouseMove(ev: MouseEvent) {
    const dx = initialPosition[0] - ev.clientX;
    const dy = initialPosition[1] - ev.clientY;

    const currRoi: ViewBox = [...roi.value];

    let newRoi: ViewBox = [
      currRoi[0],
      currRoi[1],
      initialRoi[2] - (props.pixelRatio * dx) / props.scale,
      initialRoi[3] - (props.pixelRatio * dy) / props.scale,
    ];

    if (newRoi[2] < 1) {
      newRoi[2] = 1;
    }

    if (newRoi[3] < 1) {
      newRoi[3] = 1;
    }

    if (props.constrain) {
      if (newRoi[0] + newRoi[2] > imageWidth) {
        newRoi[2] = imageWidth - newRoi[0];
      }

      if (newRoi[1] + newRoi[3] > imageHeight) {
        newRoi[3] = imageHeight - newRoi[1];
      }
    }

    newRoi = newRoi.map((val) => Math.round(val)) as ViewBox;

    let changed = false;

    newRoi.forEach((val, i) => {
      changed = changed || val !== currRoi[i];
    });

    if (changed) {
      roi.value = newRoi;
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
    <rect
      @mousedown="onMouseDownWidget"
      :x="roi[0]"
      :y="roi[1]"
      :width="roi[2]"
      :height="roi[3]"
      :stroke="borderColor"
      :fill="fillColor"
      :stroke-width="(borderSize * pixelRatio) / scale"
    />

    <rect
      @mousedown="onMouseDownHandle"
      :x="roi[0] + roi[2] - (0.5 * handleSize * pixelRatio) / scale"
      :y="roi[1] + roi[3] - (0.5 * handleSize * pixelRatio) / scale"
      :width="(handleSize * pixelRatio) / scale"
      :height="(handleSize * pixelRatio) / scale"
      :stroke="handleBorderColor"
      :fill="handleFillColor"
      :stroke-width="pixelRatio / scale"
    />
  </g>
</template>
