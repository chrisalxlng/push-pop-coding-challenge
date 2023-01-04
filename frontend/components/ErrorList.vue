<script>
import resolveConfig from "tailwindcss/resolveConfig";
import tailwindConfig from "../tailwind.config";
import ErrorListElement from "./ErrorListElement.vue";
import Button from "./Button.vue";

const fullTailwindConfig = resolveConfig(tailwindConfig);
const breakpoint = fullTailwindConfig.theme.screens.lg;

export default {
  props: {
    title: { type: String, required: true },
    errors: { type: Array, required: true },
    action: { type: Object, required: true }
  },
  components: { ErrorListElement, Button },
  data() {
    return {
      collapsed: false
    };
  },
  methods: {
    toggleCollapsed() {
      this.collapsed = !this.collapsed;
    },
    collapse() {
      this.collapsed = true;
    },
    expand() {
      this.collapsed = false;
    },
    onMediaQueryChange(mediaQueryList) {
      const matchesBreakpoint = mediaQueryList.matches;
      if (matchesBreakpoint) this.expand();
      else this.collapse();
    }
  },
  mounted() {
    const mediaQueryList = window.matchMedia(`(min-width: ${breakpoint})`);
    this.onMediaQueryChange(mediaQueryList);
  },
  beforeMount() {
    const mediaQueryList = window.matchMedia(`(min-width: ${breakpoint})`);
    mediaQueryList.addEventListener("change", () => {
      this.onMediaQueryChange(mediaQueryList);
    });
  },
  beforeDestroy() {
    const mediaQueryList = window.matchMedia(`(min-width: ${breakpoint})`);
    mediaQueryList.removeEventListener("change", () => {
      this.onMediaQueryChange(mediaQueryList);
    });
  }
};
</script>

<template>
  <div>
    <div class="bg-gray-100 rounded-md shadow relative">
      <div
        :class="
          `lg:hidden ${!this.collapsed &&
            'hidden'} absolute bottom-0 h-16 w-full z-10 rounded-b-md bg-gradient-to-b from-transparent to-gray-100`
        "
      ></div>
      <div
        class="sticky py-3 bg-gray-100 top-60px z-40 rounded-b-md flex justify-between items-center gap-2 px-1"
      >
        <h4 class="px-3 font-bold">{{ title }} ({{ errors.length }})</h4>
        <Button
          class="lg:hidden"
          @click="toggleCollapsed"
          :label="collapsed ? 'Expand' : 'Collapse'"
          :icon="collapsed ? 'angle-down' : 'angle-up'"
        />
      </div>
      <div v-if="errors.length">
        <div
          :class="
            `${collapsed && 'h-48 overflow-y-hidden'} p-3 flex flex-col gap-3`
          "
        >
          <div v-for="error in errors" :key="error.index">
            <ErrorListElement
              class="lg:w-295px"
              @error-action="$emit('error-action', $event)"
              :index="error.index"
              :code="error.code"
              :text="error.text"
              :action="action"
            />
          </div>
        </div>
      </div>
      <div v-else>
        <div class="px-3">
          <div class="py-3 w-295px">No items available.</div>
        </div>
      </div>
    </div>
  </div>
</template>
