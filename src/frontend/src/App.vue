<template>
  <div id="app">
    {{ mining }}
    <router-view />
  </div>
</template>

<script lang="ts">
import { Vue } from "vue-property-decorator";
import { io } from "socket.io-client";
import { sha256 } from "js-sha256";
import type { Transaction } from "./types";

const socket = io("http://localhost");



export default class App extends Vue {

  get walletId(){
    return this.$store.getters.walletId
  }

  validHash (hash: string): boolean  {
      return hash.startsWith("0000", 0);
  }

  computeHash(nonce: number, transaction: Transaction): string {
    
      const toHash
      return sha256(
        `${nonce}${transaction.amount}${transaction.id}${transaction.signature}`
      );
  }

  proofOfWork(transaction: Transaction): any  {
      let nonce = 0;
      let hash = "";
      while (!this.validHash(hash) && this.$store.getters.mining) {
        hash = this.computeHash(nonce, transaction);
        nonce += 1;
      }

      return {proof: hash, nonce: nonce}
  }

  get mining() {
    const mining = this.$store.getters.mining;
    if (mining) {
      socket.on("findProof", (...args: any) => {

        console.log("Received findProof! Args:",args)
        const transaction: Transaction = {
          "to": args[0].to,
          "from": args[0].from,
          "amount": parseFloat(args[0].amount),
          "id": args[0].id,
          "signature": args[0].signature,
        };
        console.log("About to compute hash! Using:",transaction)

        const temp = this.proofOfWork(transaction);
        console.log("Finished computing hash!")
        console.log("toHash: ",`${temp.nonce}${transaction.to}${transaction.from}${transaction.amount}${transaction.id}${transaction.signature}`)

        if(this.validHash(temp.proof)){
          const toSend = {
            "proof":temp.proof,
            "nonce":temp.nonce,
            "id": transaction.id,
            "minerId": this.walletId
          }

          console.log("Sending: ",toSend)
          socket.emit("proof",toSend)
        }
      });

      socket.on("reward", (...args: any) => {
          console.log("Received reward");
          this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
      });

      socket.on("stopProof", (...args: any) => {
        console.log("Received stopProof");
        this.$store.commit('MUTATION_SET_MINING', false);

      });
    }

    return null;
  }
}
</script>

<style lang="scss">
@import "./style.scss";

body {
  background-color: $background-color;
  margin: 0px;
  padding: 0px;
  font-family: $default-font;
}
</style>
