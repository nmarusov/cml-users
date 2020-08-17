<template>
  <div id="app" class="height-100-per-cent">
    <router-view ref="routerView" />
  </div>
</template>
<script>
import axios from "axios";

let HTTP = axios.create({
  baseURL: "http://10.254.63.19:1402",
});

HTTP.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem("jwt");
    config.headers.Authorization = token ? `Bearer ${token}` : "";
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export { HTTP };

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