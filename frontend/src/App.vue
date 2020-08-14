<template>
  <div id="app" class="height-100-per-cent">
    <router-view ref="routerView" />
  </div>
</template>
<script>
export default {
  components: {},
};
</script>


<style scoped>
.height-100-per-cent {
  height: 100% !important;
  overflow: auto;
}
</style>