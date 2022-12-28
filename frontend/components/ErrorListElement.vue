<script>
export default {
  props: ["code", "text"]
};
</script>

<template>
  <div class="bg-white rounded-md p-2 shadow">
    <div>
      <span class="bg-teal-500 text-white text-xs rounded-md p-1 text-center"
        ><span class="inline-block w-4 h-4">{{ code }}</span></span
      >
      <span class="text-sm mx-1">{{ text }}</span>
    </div>
  </div>
</template>
