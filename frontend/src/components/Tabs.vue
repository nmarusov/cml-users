<template>
  <div id="form">
    <b-form-group
      id="fieldset-horizontal"
      label-cols-sm="auto"
      label-cols-lg="auto"
      label="Пользователь:"
      label-for="user-selector"
    >
      <multiselect
        v-model="user"
        :options="users"
        :allow-empty="false"
        :show-labels="false"
        placeholder="Начните вводить имя пользователя"
        label="name"
        track-by="name"
        @input="updateTables()"
      ></multiselect>
    </b-form-group>
    <b-tabs content-class="mt-3" v-model="tabIndex">
      <b-tab title="Чьи обязанности исполняет" active>
        <b-table
          :fields="substitutedFields"
          :items="substituted"
          selectable
          select-mode="multi"
          @row-selected="onRowSelected"
          responsive="sm"
        >
          <template v-slot:cell(selected)="{ rowSelected }">
            <template v-if="rowSelected">
              <b-form-checkbox checked="true" disabled></b-form-checkbox>
            </template>
            <template v-else>
              <b-form-checkbox checked="false" disabled></b-form-checkbox>
            </template>
          </template>
        </b-table>
        <b-button
          class="form-button"
          @click="confirmDelete"
          :disabled="selectedSubstituted.length == 0"
          >Удалить</b-button
        >
        <b-button
          class="form-button"
          v-b-modal.adding-substituted
          :disabled="user == undefined"
          >Добавить</b-button
        >
      </b-tab>
      <b-tab title="Кто исполняет обязанности пользователя">
        <b-table :fields="deputiesFields" :items="deputies"></b-table>
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
            :options="selectableUsers"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            :hide-selected="true"
            :show-labels="false"
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
    <b-modal
      id="confirm-delete"
      @ok="removeSubstituted"
      size="sm"
      title="Удаление замены"
      >Подтвердите, что пользователь больше не будет исполнять обязанности
      выбранных пользователей.</b-modal
    >
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
      user: undefined,
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
      addedUsers: [],
      addedStartDate: "",
      addedFinishDate: "",
    };
  },
  computed: {
    selectableUsers() {
      const contains = (id) => this.substituted.some((e) => e.id === id);

      if (this.user != undefined) {
        return this.users.filter(
          (e) => e.id !== this.user.id && !contains(e.id)
        );
      }
      return this.users.filter((e) => !contains(e.id));
    },
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
        .post(`/users/substituted/${this.user.id}/add`, this.addedUsers)
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
        .get(`/users/substituted/${this.user.id}`)
        .then((response) => {
          this.substituted = response.data.users;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateDeputies() {
      client
        .get(`/users/deputies/${this.user.id}`)
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
    confirmDelete() {
      this.$bvModal.show("confirm-delete");
    },
    removeSubstituted() {
      let users = [];

      this.selectedSubstituted.forEach((user) => {
        users.push(user.id);
      });

      client
        .post(`/users/substituted/${this.user.id}/remove`, users)
        .then((response) => {
          if (response.status != 200) {
            return;
          }

          const contains = (id) => users.some((userId) => userId === id);
          this.substituted = this.substituted.filter((e) => !contains(e.id));
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
