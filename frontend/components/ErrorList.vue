<script>
import ErrorListElement from "./ErrorListElement.vue";

export default {
  props: ["title", "errors", "action"],
  components: { ErrorListElement }
};
</script>

<template>
  <div>
    <div class="bg-gray-100 rounded-md shadow">
      <div class="sticky py-3 bg-gray-100 top-60px">
        <h4 class="px-4 font-bold">{{ title }}</h4>
      </div>
      <div class="p-4 flex flex-col gap-3">
        <div v-for="error in errors" :key="error.index">
          <ErrorListElement
            @error-action="$emit('error-action', $event)"
            :index="error.index"
            :code="error.code"
            :text="error.text"
            :action="action"
          />
        </div>
      </div>
    </div>
  </div>
</template>
