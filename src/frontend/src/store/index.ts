import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import { sha256 } from "js-sha256";
import * as ecdsa from "elliptic";

// CREATE TRANSACTION SIGNATURE

const ec = new ecdsa.ec("secp256k1");

type Transaction = {
  to: string;
  from: string;
  amount: number;
  id: string;
  signature: string;
};

const generatePrivateKey = (): string => {
  const keyPair = ec.genKeyPair();
  const privateKey = keyPair.getPrivate();
  return privateKey.toString(16);
};

const privateKey = generatePrivateKey();

const getPublicFromWallet = (): string => {
  const key = ec.keyFromPrivate(privateKey, "hex");
  return key.getPublic().encode("hex", true);
};

const publicKey = getPublicFromWallet();

const getTransactionId = (transaction: Transaction): string => {
  return sha256(
    transaction.to + transaction.from + transaction.amount
  ).toString();
};

const sign = (transaction: Transaction, privateKey: string): string => {
  const dataToSign = transaction.id;

  const key = ec.keyFromPrivate(privateKey, "hex");
  const signature: string = key
    .sign(dataToSign)
    .toDER()
    .toString(16);

  return signature;
};

// END

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loading: false,
    walletCreated: false,
    walletAmount: 0,
    walletId: publicKey,
    privateKey: privateKey,
  },
  getters: {
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
    privateKey: (state) => {
      return state.privateKey;
    },
  },
  mutations: {
    MUTATATION_SET_LOADING(state, loading) {
      state.loading = loading;
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
    ACTION_INITIALIZE_WALLET({ commit, getters }) {
      commit("MUTATATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/create", {
          "public_key": getters.walletId,
        })
        .then((response) => {
          commit("MUTATATION_SET_LOADING", false);
          commit("MUTATION_SET_WALLET_CREATED", response.data.success);
        });
    },
    ACTION_FETCH_WALLET_AMOUNT({ commit, getters }) {
      commit("MUTATATION_SET_LOADING", true);
      axios
        .post("http://localhost/wallet/amount", {
          "public_key": getters.walletId,
        })
        .then((response) => {
          commit("MUTATION_SET_WALLET_AMOUNT", response.data.amount);
        });
    },
    ACTION_SEND_TRANSACTION({ getters },  values ){
      console.log("hit transaction");
      const amount = parseFloat(values.amount);
      const recipient = values.contact;
      const from = getters.walletID;

      const id = getTransactionId({ to: "", from: from, amount: amount, id: "0", signature: "" });
      const signature = sign({ to: "", from: from, amount: amount, id: id, signature: "" }, getters.privateKey);

      axios
        .post("http://localhost/transactions/create", {
          "id": id,
          "from": from,
          "to": "",
          "amount": amount,
          "signature": signature
        })
        .then((response) => {
          if(response.data.success) {
            alert("Transaction was successful!");
          } else if(response.data.err) {
            alert("Transaction has failed.");
          }
        });
    },
  },
  modules: {},
});
