<template>
  <!-- ... other code ... -->
  <BuildComponent
    :analysis_data="analysisData"
    :analysis_loading="loading"
    @show-analysis="handleShowAnalysis"
    <!-- ... other props ... -->
  />
  <!-- ... other code ... -->
</template>

<script>
export default {
  data() {
    return {
      analysisData: {},
      loading: false,
      // ... other data
    }
  },
  methods: {
    async handleShowAnalysis(hotelName) {
      this.loading = true;
      try {
        // Replace with your actual API endpoint
        const response = await this.$axios.get(`/api/build-tour-analysis/${hotelName}`);
        this.analysisData = response.data;
      } catch (error) {
        console.error("Error fetching analysis data:", error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>