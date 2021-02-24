import axios from 'axios';
import Vue from 'vue'
import Vuex from 'vuex'

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loading: false,
    walletCreated: false,
    walletAmount: 0,
    walletId: uuidv4(),
    privateKey: uuidv4()
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_WALLET_AMOUNT (state, amount) {
      state.walletAmount = amount
    },
    // TODO: Upon account creation, generate walletId and initialize wallet in the blockchain. For now, do it on app startup
    SET_WALLET_ID (state, walletId) {
      state.walletId = walletId
    },
    SET_PRIVATE_KEY (state, privateKey) {
      state.privateKey = privateKey
    },
    // TODO: Remove once we generate walletId and initialize wallet on account creation
    SET_WALLET_CREATED (state) {
      state.walletCreated = true
    },
  },
  actions: {

    initializeWallet(context){
      context.commit('SET_LOADING',true)
    // Make API call
      // axios.get('url').then(response => {
      //   context.commit('SET_LOADING',false)
      //   context.commit('SET_LOADING',false)
      // })
      context.commit('SET_LOADING',false)
    },
    fetchWalletAmount(context){
      context.commit('SET_LOADING',true)
      // Make API call
      // axios.get('url').then(response => {
      //   context.commit('SET_LOADING',false)
      //   context.commit('SET_WALLET_AMOUNT',response.data.walletAmount)
      // })
      context.commit('SET_LOADING',false)

    }
  },
  modules: {
  }
})

