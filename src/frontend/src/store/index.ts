import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import VueToast from "vue-toast-notification";
import { sha256 } from "js-sha256";
import "vue-toast-notification/dist/theme-sugar.css";
import * as rs from "jsrsasign";
import { router } from "../main";
import type { Transaction } from "../types";
import { saveAs } from 'file-saver';
import createPersistedState from "vuex-persistedstate";
import * as Cookies from 'js-cookie'

// ---------------------------------------------------------------
//  TRANSACTION SIGNING
// ---------------------------------------------------------------

const genKeyPair = (): string[] => {
  const keyPair = rs.KEYUTIL.generateKeypair("RSA", 1024);
  return [
    rs.KEYUTIL.getPEM(keyPair.prvKeyObj, "PKCS1PRV"),
    rs.KEYUTIL.getPEM(keyPair.pubKeyObj),
  ];
};

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
const ERROR_STRING = "An error occurred. Please try again.";

export default new Vuex.Store({
  // Keeps the VueX state persistent between page reloads
  plugins: [
    createPersistedState({
      getState: (key) => Cookies.getJSON(key),
      setState: (key, state) => Cookies.set(key, state, { expires: 3, secure: true })
    })
  ],
  state: {
    loading: false,
    walletAmount: 0,
    walletId: "",
    privateKey: "",
    umnetId: "",
    password: "",
    firstName: "",
    lastName: "",
    mining: false,
    editing: false,
    findProof: false
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
    findProof: (state) => {
      return state.findProof;
    },
  },
  mutations: {
    MUTATION_SET_LOADING(state, loading) {
      state.loading = loading;
    },
    MUTATION_SET_WALLET_AMOUNT(state, amount) {
      state.walletAmount = amount;
    },
    MUTATION_SET_(state, mining) {
      state.mining = mining;
    },
    MUTATION_SET_EDITING(state, editing) {
      state.editing = editing;
    },
    MUTATION_SET_FIRST_NAME(state, firstName) {
      state.firstName = firstName;
    },
    MUTATION_SET_LAST_NAME(state, lastName) {
      state.lastName = lastName;
    },
    MUTATION_SET_PASSWORD(state, password) {
      state.password = password;
    },
    MUTATION_SET_UMNETID(state, umnetId) {
      state.umnetId = umnetId
    },
    MUTATION_SET_WALLETID(state, walletId) {
      state.walletId = walletId
    },
    MUTATION_SET_PRIVATE_KEY(state, privateKey) {
      state.privateKey = privateKey
    },
    MUTATION_SET_MINING(state, mining) {
      state.mining = mining
    },
    MUTATION_SET_FIND_PROOF(state, findProof) {
      state.mining = findProof
    }
  },
  actions: {
    ACTION_UPDATE_USER({ commit, getters }, values) {
      commit("MUTATION_SET_LOADING", true);

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
            commit("MUTATION_SET_LOADING", false);
            commit("MUTATION_SET_FIRST_NAME", firstName);
            commit("MUTATION_SET_LAST_NAME", lastName);
            commit("MUTATION_SET_PASSWORD", password);
          },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            Vue.$toast.error(message
              ,
              {
                message: message,
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          }
        );
    },
    ACTION_INITIALIZE_WALLET({ commit, getters, dispatch }) {
      commit("MUTATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/create", {
          "walletId": getters.walletId,
        })
        .then(
          () => {
            commit("MUTATION_SET_LOADING", false);
            dispatch("ACTION_FETCH_WALLET_AMOUNT");
          },
          (err) => {
            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            Vue.$toast.error(message
              ,
              {
                message: message,
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
            commit("MUTATION_SET_LOADING", false);
          }
        );
    },
    ACTION_FETCH_WALLET_AMOUNT({ commit, getters }) {
      commit("MUTATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/amount", {
          "walletId": getters.walletId,
        })
        .then(
          (response) => {
            commit("MUTATION_SET_WALLET_AMOUNT", response.data.amount);
            commit("MUTATION_SET_LOADING", false);
          },
          (err) => {
            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            Vue.$toast.error(message
              ,
              {
                message: message,
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
            commit("MUTATION_SET_LOADING", false);
          }
        );
    },
    ACTION_SEND_TRANSACTION({ getters, commit }, values) {
      const recipient = values.contact;
      const transaction: Transaction = {
        "to": recipient,
        "from": getters.walletId,
        "amount": parseFloat(values.amount),
        "id": "",
        "signature": "",
      };
      transaction.id = getTransactionId(transaction);

      transaction.signature = sign(transaction, getters.privateKey);

      commit("MUTATION_SET_LOADING", true);

      axios
        .post("http://localhost/transactions/create", {
          "from": transaction.from,
          "to": transaction.to,
          "amount": transaction.amount,
          "id": transaction.id,
          "signature": transaction.signature,
        })
        .then((response) => {
          Vue.$toast.success("Transaction sent successfully!", {
            message: "Transaction sent successfully!",
            duration: 3000,
            position: "top",
            dismissible: true,
          });
          commit("MUTATION_SET_LOADING", false);
          commit("MUTATION_SET_WALLET_AMOUNT", response.data.remaining_amount);

        },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            Vue.$toast.error(
              err.response.data.error
                ? err.response.data.error
                : ERROR_STRING,
              {
                message: err.response.data.error
                  ? err.response.data.error
                  : ERROR_STRING,
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          });
    },

    ACTION_LOGIN({ commit, dispatch }, values) {
      const umnetId = values.umnetId;
      const password = values.password;

      // Do some validation first, ensure both fields were filled out
      if (umnetId == "" || password == "") {
        // If not, return and inform user
        commit("MUTATION_SET_LOADING", false);
        Vue.$toast.warning(EMPTY_TEXT_FIELD_ERROR, {
          message: EMPTY_TEXT_FIELD_ERROR,
          duration: 3000,
          position: "top",
          dismissible: true,
        });
        return;
      }
      // If we have two valid fields, send off to auth service for login

      commit("MUTATION_SET_LOADING", true);

      axios
        .post("http://localhost/users/login", {
          "umnetID": umnetId,
          "password": password,
        })
        // Inform user whether or not login was succesfful. If it wasnt, let them know why

        .then(
          (response) => {
            commit("MUTATION_SET_LOADING", false);
            commit("MUTATION_SET_FIRST_NAME", response.data.user.first_name)
            commit("MUTATION_SET_LAST_NAME", response.data.user.last_name)
            commit("MUTATION_SET_UMNETID", umnetId)
            commit("MUTATION_SET_PASSWORD", password)
            commit("MUTATION_SET_WALLETID", response.data.user.public_key)

            // TODO: Figure out reading privateKey from file

            // let reader = new FileReader();

            // const privateKey = ""


            Vue.$toast.success("Login successful!", {
              message: "Login successful!",
              duration: 3000,
              position: "top",
              dismissible: true,
            });
            dispatch("ACTION_FETCH_WALLET_AMOUNT").then(() => {
              router.push("/home");
            });

          },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            Vue.$toast.error(message
              ,
              {
                message: message,
                duration: 3000,
                position: "top",
                dismissible: true,
              }
            );
          }
        );
    },

    ACTION_CREATE_ACCOUNT({ commit, getters, dispatch }, values) {
      commit("MUTATION_SET_LOADING", true);

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
        commit("MUTATION_SET_LOADING", false);
        Vue.$toast.warning(EMPTY_TEXT_FIELD_ERROR, {
          message: EMPTY_TEXT_FIELD_ERROR,
          duration: 3000,
          position: "top",
          dismissible: true,
        });
        return;
      }

      // If we have valid fields, send off to user service for account creation
      const keyPair = genKeyPair();
      const privateKey = keyPair[0];
      const walletId = keyPair[1];
      const privateKeyHash = sha256(`${umnetId}${password}${walletId}`)

      // TODO: Remove when we read in and set privateKey on login
      commit("MUTATION_SET_PRIVATE_KEY", privateKey)
      commit("MUTATION_SET_WALLETID", walletId)

      axios
        .post("http://localhost/users/create", {
          "first_name": firstName,
          "last_name": lastName,
          "umnetID": umnetId,
          "public_key": walletId,
          "password": password,
        })
        .then(
          () => {
            commit("MUTATION_SET_LOADING", false);

            // TODO: Uncomment when we read in and set privateKey on login
            // const blob = new Blob([`${privateKeyHash}:${privateKey}`], { type: "text/plain;charset=utf-8" });
            // saveAs(blob, "privateKeys.txt")

            dispatch("ACTION_INITIALIZE_WALLET").then(() => {

              const data = { umnetId: umnetId, password: password };

              dispatch("ACTION_LOGIN", data);
            });
          },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            Vue.$toast.error(message
              ,
              {
                message: message,
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
