<template>
  <div class="flex flex-col gap-4">
    <div class="sticky top-0 shadow z-50">
      <div class="p-4 bg-white font-mono h-60px">
        <span class="bg-teal-500 text-white rounded-md p-1">Checking Tool</span>
      </div>
    </div>
    <div class="flex gap-4 p-4 max-w-6xl mx-auto">
      <ErrorList
        title="Unresolved"
        :errors="unresolved"
        :action="{ icon: 'check', tooltip: 'Resolve' }"
        @error-action="resolve"
      />
      <ErrorList
        title="Resolved"
        :errors="resolved"
        :action="{ icon: 'xmark', tooltip: 'Unresolve' }"
        @error-action="unresolve"
      />
      <ErrorList
        title="Backlog"
        :errors="backlog"
        :action="{ icon: 'plus', tooltip: 'Activate' }"
        @error-action="activate"
      />
    </div>
    <div class="p-4">
      A coding challenge submission by Christopher Lang for axess Intelligence.
    </div>
  </div>
</template>

<script>
import ErrorList from "../components/ErrorList.vue";

export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists"
      );
      return {
        resolved,
        unresolved,
        backlog
      };
    } catch (error) {
      console.log(
        `Couldn't get error lists:\n${error}\nDid you start the API?`
      );
      console.log(
        "HINT: You can comment out the full `asyncData` method and work with mocked data for UI/UX development, if you want to."
      );
    }
  },
  data() {
    return {
      resolved: [],
      unresolved: [],
      backlog: []
    };
  },
  components: { ErrorList },
  methods: {
    resolve(index) {
      const errorToResolveIndex = this.unresolved.findIndex(
        error => error.index === index
      );
      const errorToResolve = this.unresolved[errorToResolveIndex];
      this.unresolved.splice(errorToResolveIndex, 1);
      this.resolved = [...this.resolved, errorToResolve];
    },
    unresolve(index) {
      const errorToUnresolveIndex = this.resolved.findIndex(
        error => error.index === index
      );
      const errorToUnresolve = this.resolved[errorToUnresolveIndex];
      this.resolved.splice(errorToUnresolveIndex, 1);
      this.unresolved = [...this.unresolved, errorToUnresolve];
    },
    activate(index) {
      const errorToActivateIndex = this.backlog.findIndex(
        error => error.index === index
      );
      const errorToActivate = this.backlog[errorToActivateIndex];
      this.backlog.splice(errorToActivateIndex, 1);
      this.unresolved = [...this.unresolved, errorToActivate];
    }
  }
};
</script>
