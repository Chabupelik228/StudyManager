<script setup lang="ts">
interface Props {
  type?: 'card' | 'row' | 'duty' | 'stat';
  count?: number;
}

withDefaults(defineProps<Props>(), {
  type: 'card',
  count: 1,
});
</script>

<template>
  <div class="space-y-3 w-full animate-fade-in">
    <!-- Lesson Card Skeleton -->
    <template v-if="type === 'card'">
      <div
        v-for="i in count"
        :key="'card-' + i"
        class="premium-card rounded-2xl p-4 flex flex-col space-y-3"
      >
        <div class="flex items-center justify-between">
          <div class="h-6 w-20 rounded-lg skeleton-shimmer"></div>
          <div class="h-5 w-16 rounded-full skeleton-shimmer"></div>
        </div>
        <div class="space-y-2">
          <div class="h-5 w-4/5 rounded-md skeleton-shimmer"></div>
          <div class="h-4 w-1/2 rounded-md skeleton-shimmer"></div>
        </div>
        <div class="pt-2 flex items-center justify-between border-t border-app-border">
          <div class="h-4 w-28 rounded-md skeleton-shimmer"></div>
          <div class="h-5 w-5 rounded-md skeleton-shimmer"></div>
        </div>
      </div>
    </template>

    <!-- Student Attendance Row Skeleton -->
    <template v-else-if="type === 'row'">
      <div
        v-for="i in count"
        :key="'row-' + i"
        class="premium-card rounded-2xl p-3 flex items-center justify-between"
      >
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl skeleton-shimmer flex-shrink-0"></div>
          <div class="space-y-1.5">
            <div class="h-4 w-32 rounded-md skeleton-shimmer"></div>
            <div class="h-3 w-20 rounded-md skeleton-shimmer"></div>
          </div>
        </div>
        <div class="h-9 w-12 rounded-xl skeleton-shimmer"></div>
      </div>
    </template>

    <!-- Duty Row Skeleton -->
    <template v-else-if="type === 'duty'">
      <div
        v-for="i in count"
        :key="'duty-' + i"
        class="premium-card rounded-2xl p-3.5 flex items-center justify-between"
      >
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl skeleton-shimmer flex-shrink-0"></div>
          <div class="space-y-1">
            <div class="h-4 w-36 rounded-md skeleton-shimmer"></div>
            <div class="h-3 w-24 rounded-md skeleton-shimmer"></div>
          </div>
        </div>
        <div class="h-7 w-7 rounded-lg skeleton-shimmer"></div>
      </div>
    </template>

    <!-- Stat Card Skeleton -->
    <template v-else-if="type === 'stat'">
      <div
        v-for="i in count"
        :key="'stat-' + i"
        class="premium-card rounded-2xl p-4 space-y-3"
      >
        <div class="flex items-center justify-between">
          <div class="h-5 w-36 rounded-md skeleton-shimmer"></div>
          <div class="h-4 w-4 rounded-md skeleton-shimmer"></div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div class="h-16 rounded-xl skeleton-shimmer"></div>
          <div class="h-16 rounded-xl skeleton-shimmer"></div>
        </div>
      </div>
    </template>
  </div>
</template>
