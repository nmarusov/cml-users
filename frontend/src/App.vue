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


<style lang="scss">
// Import Bootstrap and BootstrapVue source SCSS files
@import "~bootstrap/scss/bootstrap.scss";
@import "~bootstrap-vue/src/index.scss";

$enable-shadows: true;

body {
  font-family: "Open Sans", sans-serif !important;
}
.height-100-per-cent {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  line-height: 1.42857143;
  color: #333;
  box-sizing: border-box;
  --toggle-checked-color: #eba079;
  --toggle-not-checked-color: var(--toggle-checked-color);
  --toggle-checked-border-color: var(--toggle-checked-color);
  --toggle-not-checked-border-color: var(--toggle-checked-color);
  font-size: 13px;
  background: #f7f7f7;
  font-family: "Open Sans", sans-serif !important;
  height: 100%;
  overflow: auto;
  animation: fade 1s;
  display: flex;
  flex-direction: column;
  flex: 0 0 auto;
  margin: 0;
}
</style>