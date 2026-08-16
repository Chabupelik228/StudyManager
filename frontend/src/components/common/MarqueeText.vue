<script setup lang="ts">
/**
 * MarqueeText — плавная прокрутка текста если он не помещается в контейнер.
 * Если текст умещается — отображается статично, без анимации.
 */
import { ref, onMounted, onUnmounted, watch, nextTick, useAttrs } from 'vue';

const props = withDefaults(
  defineProps<{
    text: string;
    speed?: number;
    pauseMs?: number;
  }>(),
  { speed: 40, pauseMs: 1500 }
);

// Forward class/style attrs to our container div manually
const attrs = useAttrs();

const containerRef = ref<HTMLDivElement | null>(null);
const innerRef = ref<HTMLSpanElement | null>(null);
const isOverflowing = ref(false);
const animating = ref(false);
let raf: number | null = null;
let startTime: number | null = null;
let phase: 'pause-start' | 'scroll' | 'pause-end' | 'reset' = 'pause-start';
let scrollDistance = 0;
let currentX = 0;

function stopAnimation() {
  if (raf !== null) {
    cancelAnimationFrame(raf);
    raf = null;
  }
}

function resetPosition() {
  if (innerRef.value) {
    innerRef.value.style.transform = 'translateX(0)';
  }
  currentX = 0;
}

async function checkOverflow() {
  stopAnimation();
  resetPosition();
  animating.value = false;

  await nextTick();

  const container = containerRef.value;
  const inner = innerRef.value;
  if (!container || !inner) return;

  // Compare scrollWidth vs clientWidth
  if (inner.scrollWidth > container.clientWidth + 2) {
    isOverflowing.value = true;
    scrollDistance = inner.scrollWidth - container.clientWidth;
    startMarquee();
  } else {
    isOverflowing.value = false;
  }
}

function startMarquee() {
  animating.value = true;
  phase = 'pause-start';
  startTime = null;
  currentX = 0;
  resetPosition();
  raf = requestAnimationFrame(tick);
}

function tick(timestamp: number) {
  if (!innerRef.value) return;

  if (startTime === null) startTime = timestamp;
  const elapsed = timestamp - startTime;

  if (phase === 'pause-start') {
    if (elapsed >= props.pauseMs) {
      phase = 'scroll';
      startTime = timestamp;
    }
  } else if (phase === 'scroll') {
    const progress = ((elapsed / 1000) * props.speed);
    currentX = Math.min(progress, scrollDistance);
    innerRef.value.style.transform = `translateX(-${currentX}px)`;

    if (currentX >= scrollDistance) {
      phase = 'pause-end';
      startTime = timestamp;
    }
  } else if (phase === 'pause-end') {
    if (elapsed >= props.pauseMs) {
      phase = 'reset';
      startTime = timestamp;
    }
  } else if (phase === 'reset') {
    // Quick snap back
    resetPosition();
    phase = 'pause-start';
    startTime = timestamp;
  }

  raf = requestAnimationFrame(tick);
}

onMounted(() => checkOverflow());
onUnmounted(() => stopAnimation());
watch(() => props.text, () => checkOverflow(), { flush: 'post' });
</script>

<script lang="ts">
export default { inheritAttrs: false };
</script>

<template>
  <div ref="containerRef" class="overflow-hidden relative" v-bind="attrs">
    <span
      ref="innerRef"
      class="inline-block whitespace-nowrap will-change-transform"
      :class="{ 'pr-8': isOverflowing }"
    >{{ text }}</span>
  </div>
</template>
