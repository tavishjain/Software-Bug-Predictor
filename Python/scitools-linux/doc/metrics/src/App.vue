<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center headline">
        {{ pageName }}
      </div>
    </v-app-bar>

    <v-content>
      <v-container
              class="body-1"
              fluid
      >
        <MetricDefinitions></MetricDefinitions>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import MetricDefinitions from "./components/MetricDefinitions";
import {mapState} from "vuex";

export default {
  name: 'App',

  components: {
    MetricDefinitions,
  },

  data: () => ({
    //
  }),
  computed: {
    ...mapState(['pageName'])

  }
};
</script>
