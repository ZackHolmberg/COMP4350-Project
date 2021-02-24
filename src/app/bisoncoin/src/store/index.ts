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

export default new Vuex.Store({
  state: {
    walletId: publicKey,
    privateKey: privateKey,
  },
  getters: {
    walletId: (state) => {
      return state.walletId;
    },
    privateKey: (state) => {
      return state.privateKey;
    },
  },
  mutations: {
  },
  actions: {
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
  modules: {
  }
})
