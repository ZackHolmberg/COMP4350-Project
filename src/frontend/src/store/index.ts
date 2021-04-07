import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import VueToast from "vue-toast-notification";
import { sha256 } from "js-sha256";
import "vue-toast-notification/dist/theme-sugar.css";
import * as rs from "jsrsasign";
import { router } from "../main";
import type { Transaction } from "../types";
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
    transaction.to + transaction.from + transaction.amount + transaction.timestamp
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
    privateKey: "",
    umnetId: "",
    password: "",
    firstName: "",
    lastName: "",
    mining: false,
    findProof: false,
    transactions: [],
  },
  getters: {
    loading: (state) => {
      return state.loading;
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
    findProof: (state) => {
      return state.findProof;
    },
    transactions: (state) => {
      return state.transactions;
    }
  },
  mutations: {
    MUTATION_SET_LOADING(state, loading) {
      state.loading = loading;
    },
    MUTATION_SET_WALLET_AMOUNT(state, walletAmount) {
      state.walletAmount = walletAmount;
    },
    MUTATION_SET_(state, mining) {
      state.mining = mining;
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
      state.umnetId = umnetId;
    },
    MUTATION_SET_PRIVATE_KEY(state, privateKey) {
      state.privateKey = privateKey;
    },
    MUTATION_SET_MINING(state, mining) {
      state.mining = mining;
    },
    MUTATION_SET_FIND_PROOF(state, findProof) {
      state.findProof = findProof;
    },
    MUTATION_SET_TRANSACTION_HISTORY(state, transactions) {
      state.transactions = transactions;
    }
  },
  actions: {
    ACTION_UPDATE_USER({ commit, getters, dispatch }, values) {
      commit("MUTATION_SET_LOADING", true);

      const password = values.password ? values.password : getters.password;
      const firstName = values.firstName ? values.firstName : getters.firstName;
      const lastName = values.lastName ? values.lastName : getters.lastName;

      axios
        .post("http://localhost/users/update", {
          "first_name": firstName,
          "last_name": lastName,
          "umnetId": getters.umnetId,
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
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'error' })
          }
        );
    },

    ACTION_FETCH_WALLET_AMOUNT({ commit, getters, dispatch }) {
      commit("MUTATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/amount", {
          "umnetId": getters.umnetId,
          "password": getters.password,
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
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'error' })
            commit("MUTATION_SET_LOADING", false);
          }
        );
    },
    ACTION_SEND_TRANSACTION({ getters, commit, dispatch }, values) {
      const recipient = values.recipient;
      const amount = values.amount
      const now = new Date()
      const utcMilllisecondsSinceEpoch = now.getTime() + (now.getTimezoneOffset() * 60 * 1000)
      const utcSecondsSinceEpoch = Math.round(utcMilllisecondsSinceEpoch / 1000)
      const transaction: Transaction = {
        "to": recipient,
        "from": getters.umnetId,
        "amount": parseFloat(amount),
        "id": "",
        "signature": "",
        "timestamp": utcSecondsSinceEpoch
      };

      transaction.id = getTransactionId(transaction);

      transaction.signature = sign(transaction, getters.privateKey);

      commit("MUTATION_SET_LOADING", true);
      axios
        .post("http://localhost/transactions/create", {
          "from": transaction.from,
          "to": transaction.to,
          "amount": transaction.amount,
          "timestamp": transaction.timestamp,
          "id": transaction.id,
          "signature": transaction.signature,
        })
        .then((response) => {

          router.push("/home");
          const message = "Transaction sent successfully!"
          dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'success' })
          commit("MUTATION_SET_LOADING", false);
          commit("MUTATION_SET_WALLET_AMOUNT", response.data.remaining_amount);

        },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'error' })
          });
    },

    ACTION_LOGIN({ commit, dispatch }, values) {
      const umnetId = values.umnetId;
      const password = values.password;

      // Do some validation first, ensure both fields were filled out
      if (umnetId == "" || password == "") {
        // If not, return and inform user
        commit("MUTATION_SET_LOADING", false);
        dispatch("ACTION_DISPLAY_TOAST", { message: EMPTY_TEXT_FIELD_ERROR, type: 'warning' })
        return;
      }
      // If we have two valid fields, send off to auth service for login

      commit("MUTATION_SET_LOADING", true);

      axios
        .post("http://localhost/users/login", {
          "umnetId": umnetId,
          "password": password,
        })
        // Inform user whether or not login was successful. If it wasn't, let them know why
        .then(
          (response) => {
            commit("MUTATION_SET_LOADING", false);
            commit("MUTATION_SET_FIRST_NAME", response.data.user.first_name)
            commit("MUTATION_SET_LAST_NAME", response.data.user.last_name)
            commit("MUTATION_SET_UMNETID", umnetId)
            commit("MUTATION_SET_PASSWORD", password)

            const privateKey = localStorage.getItem(umnetId);
            commit("MUTATION_SET_PRIVATE_KEY", privateKey)

            const message = "Login successful!"
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'success' })
            dispatch("ACTION_FETCH_WALLET_AMOUNT").then(() => {
              router.push("/home");
            });

          },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'error' })

          }
        );
    },

    ACTION_CREATE_ACCOUNT({ commit, dispatch }, values) {
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
        dispatch("ACTION_DISPLAY_TOAST", { message: EMPTY_TEXT_FIELD_ERROR, type: 'warning' })
        return;
      }

      // If we have valid fields, send off to user service for account creation
      const keyPair = genKeyPair();
      const privateKey = keyPair[0];
      const publicKey = keyPair[1];

      localStorage.setItem(umnetId, privateKey);

      axios
        .post("http://localhost/users/create", {
          "first_name": firstName,
          "last_name": lastName,
          "umnetId": umnetId,
          "public_key": publicKey,
          "password": password,
        })
        .then(
          () => {
            commit("MUTATION_SET_LOADING", false);
            commit("MUTATION_SET_WALLET_AMOUNT", 0);

            const data = { umnetId: umnetId, password: password };
            dispatch("ACTION_LOGIN", data);
          },
          (err) => {
            commit("MUTATION_SET_LOADING", false);

            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'error' })
          }
        );
    },

    ACTION_DISPLAY_TOAST({ getters }, values) {
      const message: string = values.message.toString()
      const type: string = values.type

      // Can accept an Object of options
      Vue.$toast.open({
        message: message,
        type: type,
        duration: 3000,
        position: "top",
        dismissible: true,
      });
    },

    ACTION_FETCH_TRANSACTION_HISTORY({ commit, getters, dispatch }) {
      axios
        .get("http://localhost/wallet/history/" + getters.umnetId)
        .then(
          (response) => {
            commit("MUTATION_SET_TRANSACTION_HISTORY", response.data.history);
          },
          (err) => {
            const message = err.response && err.response.data.error
              ? err.response.data.error
              : ERROR_STRING
            dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'error' })
          }
        );
    },

    ACTION_LOGOUT({ commit, dispatch }) {
      commit("MUTATION_SET_FIRST_NAME", "")
      commit("MUTATION_SET_LAST_NAME", "")
      commit("MUTATION_SET_UMNETID", "")
      commit("MUTATION_SET_PASSWORD", "")
      commit("MUTATION_SET_PRIVATE_KEY", "")
      commit("MUTATION_SET_WALLET_AMOUNT", 0)
      commit("MUTATION_SET_MINING", false)
      commit("MUTATION_SET_FIND_PROOF", false)
      commit("MUTATION_SET_TRANSACTION_HISTORY", [])

      const message = "Logout successful"
      dispatch("ACTION_DISPLAY_TOAST", { message: message, type: 'success' })
      router.push("/");

    },
  },
});
