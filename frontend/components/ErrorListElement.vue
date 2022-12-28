<script>
export default {
  props: ["index", "code", "text", "action"]
};
</script>

<template>
  <div class="bg-white rounded-md p-2 shadow">
    <div class="flex gap-1 items-center">
      <div>
        <span class="bg-teal-500 text-white text-xs rounded-md p-1 text-center"
          ><span class="inline-block w-4 h-4">{{ code }}</span></span
        >
        <span class="text-sm mx-1">{{ text }}</span>
      </div>
      <div class="tooltip">
        <button class="p-2" @click="$emit('error-action', index)">
          <Fa class="text-teal-500" :icon="['fas', action.icon]" />
          <span class="tooltip-text text-sm">{{ action.tooltip }}</span>
        </button>
      </div>
    </div>
  </div>
</template>
