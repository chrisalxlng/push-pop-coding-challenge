<script>
import Button from "./Button.vue";
import { PRIMARY } from "~/assets/js/colors";

export default {
  props: {
    index: { type: Number, required: true },
    code: { type: Number, required: true },
    text: { type: String, required: true },
    action: { type: Object, required: true }
  },
  components: { Button },
  data() {
    return {
      primaryColor: PRIMARY
    };
  }
};
</script>

<template>
  <div class="bg-white rounded-md p-2 shadow">
    <div class="flex gap-1 items-center">
      <div class="flex items-center gap-1">
        <span
          :class="
            `bg-${primaryColor} text-white text-xs rounded-md p-1 text-center`
          "
          ><span class="inline-block w-4 h-4">{{ code }}</span></span
        >
        <div class="text-sm mx-1">{{ text }}</div>
      </div>
      <Button
        @click="$emit('error-action', index)"
        :label="action.label"
        :icon="action.icon"
      />
    </div>
  </div>
</template>
