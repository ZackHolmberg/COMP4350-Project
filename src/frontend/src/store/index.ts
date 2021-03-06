import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import VueToast from "vue-toast-notification";
import { sha256 } from "js-sha256";
import "vue-toast-notification/dist/theme-sugar.css";
import * as rs from "jsrsasign";
import { router } from "../main";

// ---------------------------------------------------------------
//  TRANSACTION SIGNING
// ---------------------------------------------------------------

type Transaction = {
  to: string;
  from: string;
  amount: number;
  id: string;
  signature: string;
};

const genKeyPair = (): string[] => {
  const keyPair = rs.KEYUTIL.generateKeypair("RSA", 1024);
  return [
    rs.KEYUTIL.getPEM(keyPair.prvKeyObj, "PKCS1PRV"),
    rs.KEYUTIL.getPEM(keyPair.pubKeyObj),
  ];
};

const keyPair = genKeyPair();
const privateKey = keyPair[0];
const publicKey = keyPair[1];

const getTransactionId = (transaction: Transaction): string => {
  return sha256(
    transaction.to + transaction.from + transaction.amount
  ).toString();
};

const sign = (transaction: Transaction, privateKey: string): string => {
  const dataToSign = transaction.id;
  const sig = new rs.KJUR.crypto.Signature({ alg: "SHA256withRSA" });

  sig.init(privateKey);
  sig.updateString(dataToSign);

  return sig.sign();
};

// ---------------------------------------------------------------
// TRANSACTION SIGNING END
// ---------------------------------------------------------------

Vue.use(Vuex);
Vue.use(VueToast);

const EMPTY_TEXT_FIELD_ERROR =
  "One or more input fields are empty. Please fill out all input fields.";

export default new Vuex.Store({
  state: {
    loading: false,
    walletAmount: 0,
    walletId: publicKey,
    privateKey: privateKey,
    umnetId: "example12",
    password: "12345",
    firstName: "FirstName",
    lastName: "LastName",
    mining: false,
    editing: false,
  },
  getters: {
    loading: (state) => {
      return state.loading;
    },
    walletId: (state) => {
      return state.walletId;
    },
    walletAmount: (state) => {
      return state.walletAmount;
    },
    privateKey: (state) => {
      return state.privateKey;
    },
    umnetId: (state) => {
      return state.umnetId;
    },
    password: (state) => {
      return state.password;
    },
    firstName: (state) => {
      return state.firstName;
    },
    lastName: (state) => {
      return state.lastName;
    },
    mining: (state) => {
      return state.mining;
    },
    editing: (state) => {
      return state.editing;
    },
  },
  mutations: {
    MUTATATION_SET_LOADING(state, loading) {
      state.loading = loading;
    },
    MUTATION_SET_WALLET_AMOUNT(state, amount) {
      state.walletAmount = amount;
    },
    MUTATATION_SET_MINING(state, mining) {
      state.mining = mining;
    },
    MUTATATION_SET_EDITING(state, editing) {
      state.editing = editing;
    },
    MUTATATION_SET_FIRST_NAME(state, firstName) {
      state.firstName = firstName;
    },
    MUTATATION_SET_LAST_NAME(state, lastName) {
      state.lastName = lastName;
    },
    MUTATATION_SET_PASSWORD(state, password) {
      state.password = password;
    },
  },
  actions: {
    ACTION_UPDATE_USER({ commit, getters }, values) {
      commit("MUTATATION_SET_LOADING", true);

      const password = values.password ? values.password : getters.password;
      const firstName = values.firstName ? values.firstName : getters.firstName;
      const lastName = values.lastName ? values.lastName : getters.lastName;

      axios
        .post("http://localhost/users/update", {
          "first_name": firstName,
          "last_name": lastName,
          "umnetID": getters.umnetId,
          "public_key": getters.walletId,
          "curr_password": getters.password,
          "new_password": password
        })
        .then(
          () => {
            commit("MUTATION_SET_WALLET_CREATED", true);
            commit("MUTATATION_SET_LOADING", false);
            commit("MUTATATION_SET_FIRST_NAME", firstName);
            commit("MUTATATION_SET_LAST_NAME", lastName);
            commit("MUTATATION_SET_PASSWORD", password);


          },
          (err) => {
            commit("MUTATATION_SET_LOADING", false);
            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : "An error occurred. Please try again.",
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : "An error occurred. Please try again.",
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          }
        );
    },
    ACTION_INITIALIZE_WALLET({ commit, getters, dispatch }) {
      commit("MUTATATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/create", {
          "walletId": getters.walletId,
        })
        .then(
          () => {
            commit("MUTATION_SET_WALLET_CREATED", true);
            commit("MUTATATION_SET_LOADING", false);
            dispatch("ACTION_FETCH_WALLET_AMOUNT");
          },
          (err) => {
            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : "An error occurred. Please try again.",
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : "An error occurred. Please try again.",
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
            commit("MUTATATION_SET_LOADING", false);
          }
        );
    },
    ACTION_FETCH_WALLET_AMOUNT({ commit, getters }) {
      commit("MUTATATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/amount", {
          "walletId": getters.walletId,
        })
        .then(
          (response) => {
            commit("MUTATION_SET_WALLET_AMOUNT", response.data.amount);
            commit("MUTATATION_SET_LOADING", false);
          },
          (err) => {
            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : "An error occurred. Please try again.",
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : "An error occurred. Please try again.",
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
            commit("MUTATATION_SET_LOADING", false);
          }
        );
    },
    ACTION_SEND_TRANSACTION({ getters, dispatch, commit }, values) {
      const recipient = values.contact;
      const transaction: Transaction = {
        "to": "687", // stubbed
        "from": getters.walletId,
        "amount": parseFloat(values.amount),
        "id": "",
        "signature": "",
      };

      transaction.id = getTransactionId(transaction);
      transaction.signature = sign(transaction, getters.privateKey);
      commit("MUTATATION_SET_LOADING", true);

      axios
        .post("http://localhost/transactions/create", {
          "from": transaction.from,
          "to": transaction.to,
          "amount": transaction.amount,
          "id": transaction.id,
          "signature": transaction.signature,
        })
        .then((response) => {
          if (response.data.success) {
            Vue.$toast.success("Transaction sent successfully!", {
              message: "Transaction sent successfully!",
              duration: 3000,
              position: "top",
              dismissible: true,
            });
            commit("MUTATATION_SET_LOADING", false);
          }
        },
          (err) => {
            commit("MUTATATION_SET_LOADING", false);

            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : "An error occurred. Please try again.",
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : "An error occurred. Please try again.",
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          });
    },

    async ACTION_LOGIN({ commit, dispatch }, values) {
      const umnetId = values.umnetId;
      const password = values.password;

      // Do some validation first, ensure both fields were filled out
      if (umnetId == "" || password == "") {
        // If not, return and inform user
        commit("MUTATATION_SET_LOADING", false);
        Vue.$toast.warning(EMPTY_TEXT_FIELD_ERROR, {
          message: EMPTY_TEXT_FIELD_ERROR,
          duration: 3000,
          position: "top",
          dismissible: true,
        });
        return;
      }

      dispatch("ACTION_FETCH_WALLET_AMOUNT");

      // If we have two valid fields, send off to auth service for login

      commit("MUTATATION_SET_LOADING", true);

      axios
        .post("http://localhost/users/login", {
          "umnetID": umnetId,
          "password": password,
        })
        // Inform user whether or not login was succesfful. If it wasnt, let them know why

        .then(
          () => {
            commit("MUTATATION_SET_LOADING", false);

            Vue.$toast.success("Login successful!", {
              message: "Login successful!",
              duration: 3000,
              position: "top",
              dismissible: true,
            });
            router.push("/home");
          },
          (err) => {
            commit("MUTATATION_SET_LOADING", false);

            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : "An error occurred. Please try again.",
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : "An error occurred. Please try again.",
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          }
        );
    },

    async ACTION_CREATE_ACCOUNT({ commit, getters, dispatch }, values) {
      commit("MUTATATION_SET_LOADING", true);

      const umnetId = values.umnetId;
      const password = values.password;
      const password2 = values.password2;
      const firstName = values.firstName;
      const lastName = values.lastName;

      // Do some validation first, ensure both fields were filled out
      if (
        umnetId == "" ||
        password == "" ||
        password2 == "" ||
        firstName == "" ||
        lastName == ""
      ) {
        // If not, return and inform user
        commit("MUTATATION_SET_LOADING", false);
        Vue.$toast.warning(EMPTY_TEXT_FIELD_ERROR, {
          message: EMPTY_TEXT_FIELD_ERROR,
          duration: 3000,
          position: "top",
          dismissible: true,
        });
        return;
      }

      // If we have valid fields, send off to user service for account creation

      axios
        .post("http://localhost/users/create", {
          "firstName": firstName,
          "lastName": lastName,
          "umnetID": umnetId,
          "public_key": getters.walletId,
          "password": password,
        })
        .then(
          () => {
            commit("MUTATATION_SET_LOADING", false);

            const data = { umnetId: umnetId, password: password };
            dispatch("ACTION_INITIALIZE_WALLET").then(() => {
              dispatch("ACTION_LOGIN", data);
            });
          },
          (err) => {
            commit("MUTATATION_SET_LOADING", false);

            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : "An error occurred. Please try again.",
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : "An error occurred. Please try again.",
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          }
        );
    },
  },
});
