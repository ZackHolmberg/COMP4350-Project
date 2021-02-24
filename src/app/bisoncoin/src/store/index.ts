import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import { sha256 } from "js-sha256";
import * as ecdsa from "elliptic";

Vue.use(Vuex)

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

// Create initial Transaction object, with to/from/amount filled. Then, call getTransactionId, passing that id. Set the id of the transaction with the return value.
// Finally, call sign(), passing the transaction with 4 fields filled out and the private key, which is in the store. This returns the signature, which you will set 
// the last Transaction field (signature) too

export default new Vuex.Store({
  state: {
    walletId: publicKey,
    privateKey: privateKey,
  },
  mutations: {
  },
  actions: {
    ACTION_SEND_TRANSACTION({ commit },  values ){
      /* axios
        .post("http://localhost/wallet/create", {
          "public_key": getters.walletId,
        })
        .then((response) => {
          commit("SET_LOADING", false);
          commit("SET_WALLET_CREATED", response.data.success);
        }); */
      console.log("sent transaction "+ values.amount + values.contact);
    },
  },
  modules: {
  }
})
