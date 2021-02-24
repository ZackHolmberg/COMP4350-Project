import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import { sha256 } from "js-sha256";
import * as ecdsa from "elliptic";

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
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    SET_WALLET_AMOUNT(state, amount) {
      state.walletAmount = amount;
    },
    // TODO: Remove once we generate walletId and initialize wallet on account creation
    SET_WALLET_CREATED(state) {
      state.walletCreated = true;
    },
  },
  actions: {
    initializeWallet({ commit, getters }) {
      commit("SET_LOADING", true);
      axios
        .post("http://localhost/wallet/create", {
          "public_key": getters.walletId,
        })
        .then((response) => {
          commit("SET_LOADING", false);
          commit("SET_WALLET_CREATED", response.data.success);
        });
    },
    fetchWalletAmount({ commit, getters }) {
      commit("SET_LOADING", true);
      axios
        .post("http://localhost/wallet/amount", {
          "public_key": getters.walletId,
        })
        .then((response) => {
          commit("SET_WALLET_AMOUNT", response.data.amount);
        });
    },
  },
  modules: {},
});
