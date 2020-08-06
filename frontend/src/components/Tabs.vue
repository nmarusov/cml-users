<template>
  <div id="form">
    <b-row>
      <b-col sm="2">
        <label class="mt-3 mb-3" size="sm">Пользователь:</label>
      </b-col>
      <b-col sm="10">
        <b-form-input
          class="mt-3 mb-3"
          size="sm"
          type="search"
          v-model="filterCriteria"
          v-on:click="toggleDropDown()"
          v-on:keyup.enter="selectItem()"
          placeholder="Введите имя пользователя"
        ></b-form-input>
        <b-collapse id="drop-down">
          <b-table
            no-border-collapse
            ref="collapsibleTable"
            responsive="sm"
            selectable
            select-mode="single"
            sticky-header="200px"
            thead-class="d-none"
            v-model="filteredRows"
            :fields="selectFields"
            :filter="filterCriteria"
            :items="users"
            @row-selected="rowSelected"
          ></b-table>
        </b-collapse>
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
  baseURL: "http://10.254.63.19:1402",
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
      filterCriteria: "",
      filteredRows: [],
      selectFields: [{ key: "name", label: "Пользователь", sortable: true }],
    };
  },
  mounted() {
    client
      .get("/users/all")
      .then((response) => {
        this.users = response.data.users;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    updateTables() {
      // Получить соответствующий список пользователей
      // для указанного пользователя
      client
        .get(`/users/substituted/${this.userId}`)
        .then((response) => {
          this.substituted = response.data.users;
        })
        .catch((err) => {
          console.log(err);
        });

      client
        .get(`/users/deputies/${this.userId}`)
        .then((response) => {
          this.deputies = response.data.users;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    toggleDropDown() {
      this.$root.$emit("bv::toggle::collapse", "drop-down");
    },
    selectItem() {
      if (this.filteredRows.length === 1) {
        this.$refs.collapsibleTable.selectRow(0);
      }
    },
    rowSelected(rowArray) {
      // No rows or 1 row can be selected
      if (rowArray.length === 1) {
        this.$emit("item-selected", rowArray[0]);
        this.filterCriteria = rowArray[0].name;
        this.toggleDropDown();
        this.userId = rowArray[0].id;
        this.updateTables();
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
