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
              p-2 transform focus:translate-y-px flex items-center gap-1`
    "
    @click="$emit('click')"
  >
    <Fa :icon="['fas', icon]" />
    <span class="text-sm font-medium">{{ label }}</span>
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
