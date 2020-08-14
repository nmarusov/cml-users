<template>
  <b-container>
    <b-row align-h="center">
      <div class="apollo">
        <b-col class="apollo-container">
          <div class="apollo-facebook">Authentication</div>

          <div class="apollo-login">
            <b-form id="apollo-login-form" @submit="onSubmit">
              <b-form-group>
                <b-form-input
                  type="text"
                  name="login"
                  autocomplete="login"
                  placeholder="Login"
                  size="sm"
                  class="login-input"
                />
              </b-form-group>

              <b-form-group>
                <b-input-group size="sm">
                  <b-form-input
                    type="password"
                    name="password"
                    autocomplete="password"
                    placeholder="Password"
                    class="login-input"
                  />
                  <b-input-group-append>
                    <b-input-group-text>
                      <b-icon icon="eye-slash" aria-hidden="true"></b-icon>
                    </b-input-group-text>
                  </b-input-group-append>
                </b-input-group>
              </b-form-group>

              <b-form-group
                id="label-remember-me"
                label-cols-sm="auto"
                label-align-sm="left"
                label="Remember me"
                label-for="remember-me"
                label-size="sm"
              >
                <b-form-checkbox id="remember-me" size="sm"></b-form-checkbox>
              </b-form-group>

              <b-button type="submit" variant="outline-secondary" size="sm" block>Sign in</b-button>
            </b-form>
          </div>
        </b-col>
      </div>
    </b-row>
  </b-container>
</template>

<script>
export default {
  components: {},
  data() {
    return {};
  },
  methods: {
    onSubmit() {
      alert("Logged in!");
    },
  },
};
</script>

<style scoped>
/* Basic colors */
/* Entity colors */
/* Access Rights */
/* Page colors */
/* Statuses */
.apollo {
  top: 15%;
  display: flex;
  align-self: center;
  justify-content: center;
  width: 362px;
  border: 12px solid rgba(95, 95, 95, 0.3);
  border-radius: 5px;
  position: absolute;
  -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  -moz-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

.apollo-facebook {
  color: rgba(95, 95, 95, 0.7);
  font-size: 15px;
  font-weight: bold;
  padding-bottom: 5px;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.apollo-container .apollo-image {
  margin: 0 auto 20px auto;
  height: 115px;
  display: block;
  text-align: center;
}
.apollo-container .apollo-image img {
  height: 100%;
}

.apollo .apollo-login .v2-ui-form-group {
  min-height: 45px;
}

.apollo-container {
  padding: 20px;
  width: 100%;
  background-color: #fff;
  border-radius: 4px;
  -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  -moz-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

.apollo-container .apollo-logging-in,
.apollo-container .apollo-registering {
  text-align: center;
  display: none;
}

.apollo-container .btn-facebook {
  margin-bottom: 20px;
}

.apollo-container form {
  padding: 0;
  margin: 0;
}
.apollo-container form .ui-password-view-button {
  color: #333333;
  top: 0;
  padding: 7px;
}

#label-remember-me {
  font-weight: 500;
}

.login-input {
  border-right: none;
  border-left: none;
  border-top: none;
}

.input-group-text {
  width: 32px;
  border-right: none;
  border-left: none;
  border-top: none;
  background-color: #ffffff;
}
</style>
