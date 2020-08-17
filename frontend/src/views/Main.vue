<template>
  <div>
    <div id="nav">
      <div id="logout" v-if="isLoggedIn">
        <a @click="logout">Logout</a>
      </div>
    </div>
    <div id="form">
      <b-container>
        <b-row align-h="center">
          <b-col sm="8">
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
          </b-col>
        </b-row>

        <b-row align-h="center" align-v="stretch">
          <b-col sm="8">
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
                >Удалить</b-button>
                <b-button
                  class="form-button"
                  v-b-modal.adding-substituted
                  :disabled="user == undefined"
                >Добавить</b-button>
              </b-tab>
              <b-tab title="Кто исполняет обязанности пользователя">
                <b-table :fields="deputiesFields" :items="deputies"></b-table>
              </b-tab>
            </b-tabs>
          </b-col>
        </b-row>
      </b-container>

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
              v-model="$v.form.addedUsers.$model"
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
            >
              <template slot="selection" slot-scope="{ values, isOpen }">
                <span
                  class="multiselect__single"
                  v-if="values.length &amp;&amp; !isOpen"
                >Выбрано {{ values.length }} пользователей</span>
              </template>
            </multiselect>
            <b-form-invalid-feedback
              :force-show="!validateState('addedUsers')"
              id="users-feedback"
            >Должен быть выбран хотя бы один пользователь.</b-form-invalid-feedback>
          </b-form-group>
          <b-form-group
            label-cols-sm="4"
            label="Начальная дата:"
            label-align-sm="left"
            label-for="start-date-input"
          >
            <b-form-datepicker
              id="start-datepicker"
              v-model="$v.form.startDate.$model"
              v-bind="labels"
              class="mb-2"
              :state="validateState('startDate')"
              aria-describedby="start-date-feedback"
              placeholder="Выберите начальную дату"
            ></b-form-datepicker>
            <b-form-invalid-feedback id="start-date-feedback">Это обязательное поле.</b-form-invalid-feedback>
          </b-form-group>
          <b-form-group
            label-cols-sm="4"
            label="Конечная дата:"
            label-align-sm="left"
            label-for="finish-date-input"
          >
            <b-form-datepicker
              id="finish-datepicker"
              v-model="$v.form.finishDate.$model"
              v-bind="labels"
              class="mb-2"
              :state="validateState('finishDate')"
              aria-describedby="finish-date-feedback"
              placeholder="Выберите конечную дату"
            ></b-form-datepicker>
            <b-form-invalid-feedback
              id="finish-date-feedback"
            >Конечная дата должна быть больше или равна начальной.</b-form-invalid-feedback>
          </b-form-group>
        </form>
      </b-modal>
      <b-modal id="confirm-delete" @ok="removeSubstituted" size="sm" title="Удаление замены">
        Подтвердите, что пользователь больше не будет исполнять обязанности
        выбранных пользователей.
      </b-modal>
    </div>
  </div>
</template>

<script>
import { HTTP } from "@/App";
import Multiselect from "vue-multiselect";
import { validationMixin } from "vuelidate";
import { required, minLength } from "vuelidate/lib/validators";

function mustBeGeStartDate(value) {
  return value >= this.form.startDate;
}

export default {
  mixins: [validationMixin],
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
      form: {
        addedUsers: null,
        startDate: null,
        finishDate: null,
      },
      labels: {
        labelPrevDecade: "Предыдущая декада",
        labelPrevYear: "Предыдущий год",
        labelPrevMonth: "Предыдущий месяц",
        labelCurrentMonth: "Этот месяц",
        labelNextMonth: "Следующий месяц",
        labelNextYear: "Следующий год",
        labelNextDecade: "Следующая декада",
        labelToday: "Сегодня",
        labelSelected: "Выбранная дата",
        labelNoDateSelected: "Дата не выбрана",
        labelCalendar: "Календарь",
        labelNav: "Навигация",
        labelHelp:
          "Используйте стрелки на клавиатуре, чтобы перемещаться по датам",
      },
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
    isLoggedIn() {
      return localStorage.getItem("jwt") != null;
    },
  },
  mounted() {
    this.$root.$on("loggedIn", () => {
      if (!this.users) {
        this.getAllUsers();
      }
    });
  },
  methods: {
    logout() {
      localStorage.removeItem("jwt");

      this.users = [];
      this.substituted = [];
      this.deputies = [];

      this.$router.push("/login");
    },
    getAllUsers() {
      HTTP.get("/users/all")
        .then((response) => {
          this.users = response.data.users;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    clearAll() {
      this.form = {
        addedUsers: null,
        startDate: null,
        finishDate: null,
      };
      this.$nextTick(() => {
        this.$v.$reset();
      });
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
      this.$v.form.$touch();

      if (this.$v.form.$anyError) {
        return;
      }
      this.form.addedUsers.forEach((element) => {
        element.date_start = this.form.startDate;
        element.date_finish = this.form.finishDate;
      });

      HTTP.post(`/users/substituted/${this.user.id}/add`, this.form.addedUsers)
        .then((response) => {
          if (response.status != 200) {
            return;
          }
          this.substituted.push(...this.form.addedUsers);
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
      HTTP.get(`/users/substituted/${this.user.id}`)
        .then((response) => {
          this.substituted = response.data.users;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateDeputies() {
      HTTP.get(`/users/deputies/${this.user.id}`)
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

      HTTP.post(`/users/substituted/${this.user.id}/remove`, users)
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
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },
  },
  validations() {
    return {
      form: {
        addedUsers: {
          required,
          minLength: minLength(1),
        },
        startDate: {
          required,
        },
        finishDate: {
          required,
          mustBeGeStartDate,
        },
      },
    };
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
#form {
  margin: 5%;
}

.form-button {
  float: right;
  margin: 7px;
}

#nav {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  cursor: pointer;
}

a:hover {
  border-bottom: 1px solid;
}
</style>
