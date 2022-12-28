<script>
export default {
  props: ["index", "code", "text", "action"]
};
</script>

<template>
  <div class="bg-white rounded-md p-2 shadow">
    <div class="flex gap-1 items-center">
      <div class="flex items-center gap-1">
        <span class="bg-teal-500 text-white text-xs rounded-md p-1 text-center"
          ><span class="inline-block w-4 h-4">{{ code }}</span></span
        >
        <div class="text-sm mx-1">{{ text }}</div>
      </div>
      <button
        class="p-2 flex items-center gap-1"
        @click="$emit('error-action', index)"
      >
        <Fa class="text-teal-500" :icon="['fas', action.icon]" />
        <span class="text-sm text-teal-500 font-medium">{{
          action.label
        }}</span>
      </button>
    </div>
  </div>
</template>
