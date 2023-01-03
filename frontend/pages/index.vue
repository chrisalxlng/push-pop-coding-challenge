<template>
  <div class="flex flex-col gap-4 min-h-screen">
    <div class="sticky top-0 shadow z-50">
      <div class="flex justify-between items-center px-3 bg-white h-60px">
        <div class="p-4 font-mono">
          <span :class="`bg-${primaryColor} text-white rounded-md p-1`"
            >Checking Tool</span
          >
        </div>
        <Button
          @click="undo"
          label="Undo last action"
          icon="rotate-left"
          :isDisabled="isDisabled"
        />
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
import Button from "../components/Button.vue";
import { PRIMARY } from "~/assets/js/colors";

export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists?operator_name=John"
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
      lastActions: [],
      primaryColor: PRIMARY
    };
  },
  computed: {
    isDisabled() {
      return !this.lastActions.length;
    }
  },
  components: { Button, ErrorList },
  methods: {
    updateLastActions(inverseAction, originPosition, destinationPosition) {
      this.lastActions.push({
        inverseAction,
        originPosition,
        destinationPosition
      });
    },
    undo() {
      if (!this.lastActions.length) return;
      const {
        inverseAction,
        originPosition,
        destinationPosition
      } = this.lastActions.pop();
      inverseAction(destinationPosition, originPosition);
    },
    moveErrorFromUnresolvedToResolved(unresolvedPosition, resolvedPosition) {
      const error = this.unresolved[unresolvedPosition];
      this.unresolved.splice(unresolvedPosition, 1);

      const updatedResolved = [...this.resolved];
      updatedResolved.splice(resolvedPosition, 0, error);
      this.resolved = updatedResolved;
    },
    resolve(index) {
      const unresolvedPosition = this.unresolved.findIndex(
        error => error.index === index
      );

      this.moveErrorFromUnresolvedToResolved(
        unresolvedPosition,
        this.resolved.length
      );

      const resolvedPosition = this.resolved.findIndex(
        error => error.index === index
      );

      this.updateLastActions(
        this.moveErrorFromResolvedToUnresolved,
        unresolvedPosition,
        resolvedPosition
      );
    },
    moveErrorFromResolvedToUnresolved(resolvedPosition, unresolvedPosition) {
      const error = this.resolved[resolvedPosition];
      this.resolved.splice(resolvedPosition, 1);

      const updatedUnresolved = [...this.unresolved];
      updatedUnresolved.splice(unresolvedPosition, 0, error);
      this.unresolved = updatedUnresolved;
    },
    unresolve(index) {
      const resolvedPosition = this.resolved.findIndex(
        error => error.index === index
      );

      this.moveErrorFromResolvedToUnresolved(
        resolvedPosition,
        this.unresolved.length
      );

      const unresolvedPosition = this.unresolved.findIndex(
        error => error.index === index
      );

      this.updateLastActions(
        this.moveErrorFromUnresolvedToResolved,
        resolvedPosition,
        unresolvedPosition
      );
    },
    moveErrorFromBacklogToUnresolved(backlogPosition, unresolvedPosition) {
      const error = this.backlog[backlogPosition];
      this.backlog.splice(backlogPosition, 1);

      const updatedUnresolved = [...this.unresolved];
      updatedUnresolved.splice(unresolvedPosition, 0, error);
      this.unresolved = updatedUnresolved;
    },
    activate(index) {
      const backlogPosition = this.backlog.findIndex(
        error => error.index === index
      );

      this.moveErrorFromBacklogToUnresolved(
        backlogPosition,
        this.unresolved.length
      );

      const unresolvedPosition = this.unresolved.findIndex(
        error => error.index === index
      );

      this.updateLastActions(
        this.moveErrorFromUnresolvedToBacklog,
        backlogPosition,
        unresolvedPosition
      );
    },
    moveErrorFromUnresolvedToBacklog(unresolvedPosition, backlogPosition) {
      const error = this.unresolved[unresolvedPosition];
      this.unresolved.splice(unresolvedPosition, 1);

      const updatedBacklog = [...this.backlog];
      updatedBacklog.splice(backlogPosition, 0, error);
      this.backlog = updatedBacklog;
    }
  }
};
</script>
