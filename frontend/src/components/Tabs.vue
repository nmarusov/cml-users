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
            @row-selected="dropdownRowSelected"
          ></b-table>
        </b-collapse>
      </b-col>
    </b-row>
    <b-tabs content-class="mt-3" v-model="tabIndex">
      <b-tab title="Чьи обязанности исполняет" active>
        <b-table
          :fields="substitutedFields"
          :items="substituted"
          :keyword="userName"
          selectable
          select-mode="multi"
          @row-selected="onRowSelected"
          responsive="sm"
        >
          <template v-slot:cell(selected)="{ rowSelected }">
            <template v-if="rowSelected">
              <span aria-hidden="true">&check;</span>
              <span class="sr-only">Selected</span>
            </template>
            <template v-else>
              <span aria-hidden="true">&nbsp;</span>
              <span class="sr-only">Not selected</span>
            </template>
          </template>
        </b-table>
        <b-button
          class="form-button"
          @click="removeSubstituted"
          :disabled="selectedSubstituted.length == 0"
          >Удалить</b-button
        >
        <b-button
          class="form-button"
          v-b-modal.adding-substituted
          :disabled="userId == undefined"
          >Добавить</b-button
        >
      </b-tab>
      <b-tab title="Кто исполняет обязанности пользователя">
        <b-table
          :fields="deputiesFields"
          :items="deputies"
          :keyword="userName"
        ></b-table>
      </b-tab>
    </b-tabs>
    <b-modal
      id="adding-substituted"
      centered
      title="Добавление замены"
      @ok="handleOk"
      @cancel="handleCancel"
      @close="handleCancel"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label-cols-sm="4"
          label="Пользователи:"
          label-align-sm="left"
          label-for="name-input"
        >
          <multiselect
            v-model="addedUsers"
            :options="users"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите пользователя"
            label="name"
            track-by="name"
            :preselect-first="false"
          >
            <template slot="selection" slot-scope="{ values, isOpen }"
              ><span
                class="multiselect__single"
                v-if="values.length &amp;&amp; !isOpen"
                >Выбрано {{ values.length }} пользователей</span
              ></template
            >
          </multiselect>
        </b-form-group>
        <b-form-group
          label-cols-sm="4"
          label="Начальная дата:"
          label-align-sm="left"
          label-for="start-date-input"
        >
          <b-form-datepicker
            id="start-datepicker"
            v-model="addedStartDate"
            class="mb-2"
          ></b-form-datepicker>
        </b-form-group>
        <b-form-group
          label-cols-sm="4"
          label="Конечная дата:"
          label-align-sm="left"
          label-for="finish-date-input"
        >
          <b-form-datepicker
            id="finish-datepicker"
            v-model="addedFinishDate"
            class="mb-2"
          ></b-form-datepicker>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import Multiselect from "vue-multiselect";

const client = axios.create({
  baseURL: "http://10.254.63.19:1402",
});

export default {
  components: {
    Multiselect,
  },
  data() {
    return {
      tabIndex: 0,
      userName: "",
      userId: undefined,
      substituted: [],
      selectedSubstituted: [],
      deputies: [],
      users: [],
      deputiesFields: [
        { key: "name", label: "Пользователь", sortable: true },
        { key: "date_start", label: "Начальная дата", sortable: true },
        { key: "date_finish", label: "Конечная дата", sortable: true },
      ],
      substitutedFields: [
        { key: "selected", label: "", sortable: false },
        { key: "name", label: "Пользователь", sortable: true },
        { key: "date_start", label: "Начальная дата", sortable: true },
        { key: "date_finish", label: "Конечная дата", sortable: true },
      ],
      filterCriteria: "",
      filteredRows: [],
      selectFields: [{ key: "name", label: "Пользователь", sortable: true }],
      form: {
        email: "",
        name: "",
        food: null,
        checked: [],
      },
      addedUsers: [],
      addedStartDate: "",
      addedFinishDate: "",
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
    clearAll() {
      this.addedUsers = [];
      this.addedStartDate = "";
      this.addedFinishDate = "";
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    handleCancel() {
      this.clearAll();
    },
    handleSubmit() {
      this.addedUsers.forEach((element) => {
        element.date_start = this.addedStartDate;
        element.date_finish = this.addedFinishDate;
      });

      client
        .post(`/users/substituted/${this.userId}/add`, this.addedUsers)
        .then((response) => {
          if (response.status != 200) {
            return;
          }
          this.substituted.push(...this.addedUsers);
          this.clearAll();
        })
        .catch((err) => {
          console.log(err);
        });

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide("adding-substituted");
      });
    },
    onRowSelected(items) {
      this.selectedSubstituted = items;
    },
    updateSubstituted() {
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
    },
    updateDeputies() {
      client
        .get(`/users/deputies/${this.userId}`)
        .then((response) => {
          this.deputies = response.data.users;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateTables() {
      this.updateSubstituted();
      this.updateDeputies();
    },
    toggleDropDown() {
      this.$root.$emit("bv::toggle::collapse", "drop-down");
    },
    selectItem() {
      if (this.filteredRows.length === 1) {
        this.$refs.collapsibleTable.selectRow(0);
      }
    },
    dropdownRowSelected(rowArray) {
      // No rows or 1 row can be selected
      if (rowArray.length === 1) {
        this.$emit("item-selected", rowArray[0]);
        this.filterCriteria = rowArray[0].name;
        this.toggleDropDown();
        this.userId = rowArray[0].id;
        this.updateTables();
      }
    },
    removeSubstituted() {
      let users = [];

      this.selectedSubstituted.forEach((user) => {
        users.push(user.id);
      });

      client
        .post(`/users/substituted/${this.userId}/remove`, users)
        .then((response) => {
          if (response.status != 200) {
            return;
          }
          this.substituted.forEach((item, index) => {
            if (users.includes(item.id)) {
              this.substituted.pop(index);
            }
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
#form {
  margin: 0 auto;
  width: 1000px;
}
.form-button {
  float: right;
  margin: 7px;
}
</style>
