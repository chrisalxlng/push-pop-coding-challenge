<template>
  <button
    :disabled="isDisabled"
    :class="
      `
            ${
              isDisabled
                ? `text-${disabledColor} cursor-not-allowed`
                : `text-${primaryColor} hover:text-${primaryColorHover} cursor-pointer`
            }
              p-2 transform focus:translate-y-px`
    "
    @click="$emit('click')"
  >
    <div class=" flex items-center gap-1">
      <Fa :icon="['fas', icon]" />
      <span class="text-sm font-medium">{{ label }}</span>
    </div>
  </button>
</template>

<script>
import { PRIMARY, PRIMARY_HOVER, DISABLED } from "~/assets/js/colors";

export default {
  props: {
    label: { type: String, required: true },
    icon: { type: String, required: true },
    isDisabled: { type: Boolean, default: false }
  },
  data() {
    return {
      primaryColor: PRIMARY,
      primaryColorHover: PRIMARY_HOVER,
      disabledColor: DISABLED
    };
  }
};
</script>
