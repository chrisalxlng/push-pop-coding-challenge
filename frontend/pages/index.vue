<template>
  <div class="flex flex-col gap-4 min-h-screen">
    <div class="sticky top-0 shadow z-50">
      <div class="flex justify-between items-center px-3 bg-white h-60px">
        <div class="p-4 font-mono">
          <span class="bg-teal-500 text-white rounded-md p-1"
            >Checking Tool</span
          >
        </div>
        <button
          :disabled="isDisabled"
          :class="`${isDisabled ? 'cursor-not-allowed' : 'cursor-pointer'} p-2`"
          @click="undo"
        >
          <Fa
            :class="isDisabled ? 'text-gray-500' : 'text-teal-500'"
            :icon="['fas', 'rotate-left']"
          />
          <span
            :class="
              `${
                isDisabled ? 'text-gray-500' : 'text-teal-500'
              } text-sm font-medium`
            "
            >Undo last action</span
          >
        </button>
      </div>
    </div>
    <div class="flex flex-1 justify-center gap-3 p-4 max-w-6xl mx-auto">
      <ErrorList
        title="Unresolved"
        :errors="unresolved"
        :action="{ icon: 'check', label: 'Resolve' }"
        @error-action="resolve"
      />
      <ErrorList
        title="Resolved"
        :errors="resolved"
        :action="{ icon: 'xmark', label: 'Unresolve' }"
        @error-action="unresolve"
      />
      <ErrorList
        title="Backlog"
        :errors="backlog"
        :action="{ icon: 'plus', label: 'Activate' }"
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
      backlog: [],
      lastAction: { inverseAction: null, index: null }
    };
  },
  computed: {
    isDisabled() {
      return !this.lastAction.inverseAction || isNaN(this.lastAction.index);
    }
  },
  components: { ErrorList },
  methods: {
    updateLastAction(inverseAction, index) {
      this.lastAction = { inverseAction, index };
    },
    undo() {
      const { inverseAction, index } = this.lastAction;
      inverseAction(index);
      this.updateLastAction(null, null);
    },
    resolve(index) {
      const errorToResolveIndex = this.unresolved.findIndex(
        error => error.index === index
      );
      const errorToResolve = this.unresolved[errorToResolveIndex];
      this.unresolved.splice(errorToResolveIndex, 1);
      this.resolved = [...this.resolved, errorToResolve];
      this.updateLastAction(this.unresolve, index);
    },
    unresolve(index) {
      const errorToUnresolveIndex = this.resolved.findIndex(
        error => error.index === index
      );
      const errorToUnresolve = this.resolved[errorToUnresolveIndex];
      this.resolved.splice(errorToUnresolveIndex, 1);
      this.unresolved = [...this.unresolved, errorToUnresolve];
      this.updateLastAction(this.resolve, index);
    },
    activate(index) {
      const errorToActivateIndex = this.backlog.findIndex(
        error => error.index === index
      );
      const errorToActivate = this.backlog[errorToActivateIndex];
      this.backlog.splice(errorToActivateIndex, 1);
      this.unresolved = [...this.unresolved, errorToActivate];
      this.updateLastAction(this.unactivate, index);
    },
    unactivate(index) {
      const errorToUnactivateIndex = this.unresolved.findIndex(
        error => error.index === index
      );
      const errorToUnactivate = this.unresolved[errorToUnactivateIndex];
      this.unresolved.splice(errorToUnactivateIndex, 1);
      this.backlog = [...this.backlog, errorToUnactivate];
      this.updateLastAction(this.activate, index);
    }
  }
};
</script>
