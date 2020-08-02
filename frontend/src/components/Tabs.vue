<template>
  <div id="form">
    <b-row class="my-1">
      <b-col sm="2">
        <label class="mt-3 mb-3" size="sm">Пользователь:</label>
      </b-col>
      <b-col sm="10">
        <b-input-group class="mt-3 mb-3" size="sm">
          <b-form-input
            id="userName"
            v-model="userName"
            v-on:change="onNameChange"
            placeholder="Введите имя пользователя"
          ></b-form-input>
          <b-input-group-append>
            <b-button>...</b-button>
          </b-input-group-append>
        </b-input-group>
      </b-col>
    </b-row>
    <b-tabs content-class="mt-3" v-model="tabIndex">
      <b-tab title="Чьи обязанности исполняет" active>
        <b-table :fields="fields" :items="substituted" :keyword="userName"></b-table>
      </b-tab>
      <b-tab title="Кто исполняет обязанности пользователя" lazy>
        <b-table :fields="fields" :items="deputies" :keyword="userName"></b-table>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:1402",
});

export default {
  components: {},
  data() {
    return {
      tabIndex: 0,
      userName: "",
      userId: undefined,
      substituted: [],
      deputies: [],
      users: [],
      fields: [
        { key: "name", label: "Пользователь", sortable: true },
        { key: "date_start", label: "Начальная дата", sortable: true },
        { key: "date_finish", label: "Конечная дата", sortable: true },
      ],
    };
  },
  mounted() {
    client
      .get("/all")
      .then((response) => {
        this.users = response.data.users;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    onNameChange: function () {
      // Определить ID пользователя по его имени
      this.userId = undefined;

      for (let i = 0; i < this.users.length; i++) {
        if (this.users[i].name == this.userName) {
          this.userId = this.users[i].id;
          break;
        }
      }

      // Выдать сообщение об ошибке, если пользователь не найден
      if (this.userId == undefined) {
        alert(`Пользователь ${this.userName} не существует.`);
      }

      // Получить соответствующий список пользователей
      // для указанного пользователя
      if (this.tabIndex == 0) {
        client
          .get(`/substituted/${this.userId}`)
          .then((response) => {
            this.substituted = response.data.users;
          })
          .catch((err) => {
            console.log(err);
          });
      } else if (this.tabIndex == 1) {
        client
          .get(`/deputies/${this.userId}`)
          .then((response) => {
            this.deputies = response.data.users;
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
};
</script>
<style scoped>
#form {
  margin: 0 auto;
  width: 1000px;
}
</style>
