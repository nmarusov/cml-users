<template>
  <div id="app" class="height-100-per-cent">
    <router-view ref="routerView" />
  </div>
</template>
<script>
import axios from "axios";

export const HTTP = axios.create({
  baseURL: "http://10.254.63.19:1402",
});

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