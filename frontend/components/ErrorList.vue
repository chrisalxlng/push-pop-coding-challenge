<script>
import ErrorListElement from "./ErrorListElement.vue";

export default {
  props: {
    title: { type: String, required: true },
    errors: { type: Array, required: true },
    action: { type: Object, required: true }
  },
  components: { ErrorListElement }
};
</script>

<template>
  <div>
    <div class="bg-gray-100 rounded-md shadow">
      <div class="sticky py-3 bg-gray-100 top-60px z-40">
        <h4 class="px-3 font-bold">{{ title }} ({{ errors.length }})</h4>
      </div>
      <div v-if="errors.length">
        <div class="p-3 flex flex-col gap-3">
          <div v-for="error in errors" :key="error.index">
            <ErrorListElement
              class="w-295px"
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
