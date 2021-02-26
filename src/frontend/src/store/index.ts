import axios from "axios";
import Vue from "vue";
import Vuex from "vuex";
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';

type Transaction = {
  to: string;
  from: string;
  amount: number;
};

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

Vue.use(Vuex);
Vue.use(VueToast);

export default new Vuex.Store({
  state: {
    loading: false,
    walletCreated: false,
    walletAmount: 0,
    walletId: uuidv4(),
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
    ACTION_SEND_TRANSACTION({ getters, dispatch },  values ){
      const recipient = values.contact;
      const transaction: Transaction = { 
        to: "687", // stubbed
        from: getters.walletId, 
        amount: parseFloat(values.amount), 
      };
    
      axios
        .post("http://localhost/transactions/create", {
          "from": transaction.from,
          "to": transaction.to,
          "amount": transaction.amount,
        })
        .then((response) => {
          if(response.data.success) {
            Vue.$toast.success('Transaction has sent!', {
              message: 'Transaction has sent!',
              duration: 3000,
              position: 'top',
              dismissible: true,
            });

            dispatch("ACTION_FETCH_WALLET_AMOUNT");
          } else if(response.data.err) {
            Vue.$toast.error('Transaction has failed.', { 
              message: 'Transaction has failed', 
              duration: 3000, 
              position: 'top',
              dismissible: true, 
            });
          }
        });
    },
  },
});
