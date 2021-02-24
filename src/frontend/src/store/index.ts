import axios from 'axios';
import Vue from 'vue'
import Vuex from 'vuex'
import { sha256 } from 'js-sha256';

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

const getTransactionId = (transaction:Transaction): string => {
  const txInContent: string = transaction.txIns
      .map((txIn: TxIn) => txIn.txOutId + txIn.txOutIndex)
      .reduce((a, b) => a + b, '');

  const txOutContent: string = transaction.txOuts
      .map((txOut: TxOut) => txOut.address + txOut.amount)
      .reduce((a, b) => a + b, '');

  return CryptoJS.SHA256(txInContent + txOutContent).toString();
};

// def sign():

//     data = request.get_json()
//     try: 
//         to_sign = data["to_sign"]


//     # TODO: when the user service and auth service is implemented make the appropriate calls
//     # to get the current user instead of client passing it into the json data

//         user = data["user"]


//     # Retrieve the private key from the database

//         key = keys[user]

//     except Exception as ex:
//         return jsonify(Exception=ex), HttpCode.BAD_REQUEST


//     signing_key = SigningKey.from_string(bytes.fromhex(key))
//     signature = signing_key.sign(to_sign)

//     return jsonify(to_sign=tosign, signature=signature), HttpCode.OK

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
      // axios.get('http://localhost/wallet').then(response => {
      //   context.commit('SET_LOADING',false)
      //   context.commit('SET_WALLET_AMOUNT',response.data.walletAmount)
      // })
      const temp = uuidv4()
      context.commit('SET_WALLET_AMOUNT',temp)
      context.commit('SET_LOADING',false)

    }
  },
  modules: {
  }
})

