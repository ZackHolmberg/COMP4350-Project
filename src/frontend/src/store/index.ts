import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import VueToast from 'vue-toast-notification';
import { sha256 } from "js-sha256";
import 'vue-toast-notification/dist/theme-sugar.css';
import * as rs from 'jsrsasign';

type Transaction = {
  to: string;
  from: string;
  amount: number;
  id: string;
  signature: string;
};

// Transaction Signing
const genKeyPair = (): string[] => {
  const keyPair = rs.KEYUTIL.generateKeypair("RSA", 1024);
  console.log(keyPair)
  return [rs.KEYUTIL.getPEM(keyPair.prvKeyObj, "PKCS1PRV"), rs.KEYUTIL.getPEM(keyPair.pubKeyObj)];
}

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
  const sig = new rs.KJUR.crypto.Signature({alg: 'SHA256withRSA'})

  sig.init(privateKey);
  sig.updateString(dataToSign);

  return sig.sign();
};
// end 

Vue.use(Vuex);
Vue.use(VueToast);

export default new Vuex.Store({
  state: {
    loading: false,
    walletCreated: false,
    walletAmount: 0,
    walletId: publicKey,//uuidv4(),
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
          "walletId": getters.walletId,
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
          "walletId": getters.walletId,
        })
        .then((response) => {
          commit("MUTATION_SET_WALLET_AMOUNT", response.data.amount);
        });
    },
    ACTION_SEND_TRANSACTION({ getters, commit },  values ){
      const recipient = values.contact;
      const transaction: Transaction = { 
        to: "687", // stubbed
        from: getters.walletId, 
        amount: parseFloat(values.amount),
        id: "",
        signature: ""
      };
    
      transaction.id = getTransactionId(transaction) 
      transaction.signature = sign(transaction, getters.privateKey)

      axios
        .post("http://localhost/transactions/create", {
          "from": transaction.from,
          "to": transaction.to,
          "amount": transaction.amount,
          "id": transaction.id,
          "signature": transaction.signature
        })
        .then((response) => {
          if(response.data.success) {
            Vue.$toast.success('Transaction has been sent!', {
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
  },
});
