import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';
import { router } from "../main";

type Transaction = {
  to: string;
  from: string;
  amount: number;
};

function uuidv4() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
    const r = (Math.random() * 16) | 0,
      v = c == "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

Vue.use(Vuex);
Vue.use(VueToast);

const EMPTY_TEXT_FIELD_ERROR =
  "One or more input fields are empty. Please fill out all input fields.";

export default new Vuex.Store({
  state: {
    loading: false,
    walletCreated: false,
    walletAmount: 0,
    walletId: uuidv4(),
    userError: null,
  },
  getters: {
    loading: (state) => {
      return state.loading;
    },
    userError: (state) => {
      return state.userError;
    },
    walletId: (state) => {
      return state.walletId;
    },
    walletAmount: (state) => {
      return state.walletAmount;
    },
    // TODO: Remove this getter once we initialize wallet on account creation and not in wallet component
    walletCreated: (state) => {
      return state.walletCreated;
    },
  },
  mutations: {
    MUTATATION_SET_LOADING(state, loading) {
      state.loading = loading;
    },
    MUTATATION_SET_USER_ERROR(state, userError) {
      state.userError = userError;
    },
    MUTATION_SET_WALLET_AMOUNT(state, amount) {
      state.walletAmount = amount;
    },
    // TODO: Remove once we generate walletId and initialize wallet on account creation
    MUTATION_SET_WALLET_CREATED(state) {
      state.walletCreated = true;
    },
  },
  actions: {
    ACTION_INITIALIZE_WALLET({ commit, getters, dispatch }) {
      commit("MUTATATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/create", {
          walletId: getters.walletId,
        })
        .then((response) => {
          if (response.status == 201) {
            commit("MUTATATION_SET_LOADING", false);
            commit("MUTATION_SET_WALLET_CREATED", true);
            dispatch("ACTION_FETCH_WALLET_AMOUNT");
          } else {
            commit(
              "MUTATATION_SET_USER_ERROR",
              response.data.error
                ? response.data.error
                : "An error occurred. Please try again."
            );
          }
        });
    },
    ACTION_FETCH_WALLET_AMOUNT({ commit, getters }) {
      commit("MUTATATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/amount", {
          walletId: getters.walletId,
        })
        .then((response) => {
          if (response.status == 200) {
            commit("MUTATION_SET_WALLET_AMOUNT", response.data.amount);
          } else {
            commit(
              "MUTATATION_SET_USER_ERROR",
              response.data.error
                ? response.data.error
                : "An error occurred. Please try again."
            );
          }
        });
    },
    ACTION_SEND_TRANSACTION({ getters, dispatch, commit }, values) {
      const recipient = values.contact;
      const transaction: Transaction = {
        to: "687", // stubbed
        from: getters.walletId,
        amount: parseFloat(values.amount),
      };

      axios
        .post("http://localhost/transactions/create", {
          from: transaction.from,
          to: transaction.to,
          amount: transaction.amount,
        })
        .then((response) => {
          if(response.data.success) {
            Vue.$toast.success('Transaction has sent!', {
              message: 'Transaction has sent!',
              duration: 3000,
              position: 'top',
              dismissible: true,
            });
            commit("MUTATION_SET_WALLET_AMOUNT", response.data.remaining_balance);
          } 
        }, (err) => {
          Vue.$toast.error(err.response.data.err, { 
            message: err.response.data.err, 
            duration: 3000, 
            position: 'top',
            dismissible: true, 
          });
        }); 
    },

    async ACTION_LOGIN({ commit, getters, dispatch }, values) {
      commit("MUTATATION_SET_LOADING", true);

      console.log(values);
      const umnetId = values.umnetId;
      const password = values.password;

      // Do some validation first, ensure both fields were filled out
      if (umnetId == "" || password == "") {
        commit("MUTATATION_SET_LOADING", false);
        commit("MUTATATION_SET_USER_ERROR", EMPTY_TEXT_FIELD_ERROR);
        return;
      }
      // If not, return and inform user

      // If we have two valid fields, send off to auth service for login
      await sleep(3000);
      router.push("/home");

      // Inform user whether or not login was succesfful. If it wasnt, let them know why

      // axios
      //   .post("http://localhost/users/login", {
      //     umnetId: umnetId,
      //     password: password,
      //   })
      //   .then((response) => {
      //     if (response.status == 200) {
      //       router.push("/home");
      //     } else {
      //       commit("MUTATATION_SET_LOADING", false);
      //       commit(
      //         "MUTATATION_SET_USER_ERROR",
      //         response.data.err
      //           ? response.data.err
      //           : "An error occurred. Please try again."
      //       );
      //     }
      //   });

      commit("MUTATATION_SET_LOADING", false);
    },

    async ACTION_CREATE_ACCOUNT({ commit, getters, dispatch }, values) {
      commit("MUTATATION_SET_LOADING", true);

      const umnetId = values.umnetId;
      const password = values.password; // Should probably get encrypted?
      const password2 = values.password2;
      const firstName = values.firstName;
      const lastName = values.lastName;

      // Do some validation first, ensure both fields were filled out
      if (
        umnetId != "" &&
        password != "" &&
        password2 != "" &&
        firstName != "" &&
        lastName != ""
      ) {
        // If not, return and inform user
        commit("MUTATATION_SET_LOADING", false);
        commit("MUTATATION_SET_USER_ERROR", EMPTY_TEXT_FIELD_ERROR);
        return;
      }

      // If we have valid fields, send off to auth service for account creation
      await sleep(3000);
      dispatch("ACTION_INITIALIZE_WALLET");

      // axios
      //   .post("http://localhost/users/create", {
      //     umnetId: umnetId,
      //     password: password,
      //     firstName: firstName,
      //     lastName: lastName,
      //   })
      //   .then((response) => {
      //     if (response.status == 201) {
      //       const data = { umnetId: umnetId, password: password };
      //       dispatch("ACTION_LOGIN", data);
      // dispatch("ACTION_INITIALIZE_WALLET");

      //     } else {
      //       commit("MUTATATION_SET_LOADING", false);
      //       commit(
      //         "MUTATATION_SET_USER_ERROR",
      //         response.data.err
      //           ? response.data.err
      //           : "An error occurred. Please try again."
      //       );
      //     }
      //   });
    },
  },
});
