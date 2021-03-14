<template>
  <div id="app">
    {{ mining }}
    <router-view />
  </div>
</template>

<script lang="ts">
import { Vue } from "vue-property-decorator";
import { io, Socket } from "socket.io-client";
import { sha256 } from "js-sha256";
import type { Transaction } from "./types";
import { DefaultEventsMap } from "socket.io-client/build/typed-events";

let socket: Socket<DefaultEventsMap, DefaultEventsMap>;

export default class App extends Vue {

  get walletId(){
    return this.$store.getters.walletId
  }

  get findProof(){
    return this.$store.getters.findProof
  }

  validHash (hash: string): boolean  {
      return hash.startsWith("0000", 0);
  }

  computeHash(nonce: number, transaction: Transaction): string {

      const toHash = (nonce.toString()+transaction.amount.toString()+transaction.id+transaction.signature).replace(/(\r\n|\n|\r)/gm, "");
      return sha256(toHash);
  }

  proofOfWork(transaction: Transaction): any  {
      let nonce = -1;
      let hash = "";
      while (!this.validHash(hash) && this.findProof) {
        nonce += 1;
        hash = this.computeHash(nonce, transaction);
      }
      // console.log("Returning: ",{proof: hash, nonce: nonce})
      return {proof: hash, nonce: nonce}
  }


  get mining() {
    const mining = this.$store.getters.mining;
    if (mining) {
      if(!socket){
        socket = io("http://localhost");
      }
      if(!socket.connected){
        socket.connect()
      }

      socket.on("findProof", (...args: any) => {

        // console.log("Received findProof! Args:",args)
        this.$store.commit('MUTATION_SET_FIND_PROOF', true);

        const transaction: Transaction = {
          "to": args[0].to,
          "from": args[0].from,
          "amount": parseFloat(args[0].amount),
          "id": args[0].id,
          "signature": args[0].signature,
        };
        // console.log("About to compute hash! Using:",transaction)

        const temp = this.proofOfWork(transaction);
        // console.log("Finished computing hash!")
        // console.log("used the following to compute hash: ",(temp.nonce+transaction.amount+transaction.id+transaction.signature).replace(/(\r\n|\n|\r)/gm, ""))

        if(this.validHash(temp.proof)){
          const toSend = {
            "proof":temp.proof,
            "nonce":temp.nonce,
            "id": transaction.id,
            "minerId": this.walletId
          }

          // console.log("Sending: ",toSend)
          socket.emit("proof",toSend)
          this.$store.commit('MUTATION_SET_FIND_PROOF', false);

        }
      });

      socket.on("reward", () => {
          console.log("Received reward");
          this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
      });

      socket.on("stopProof", () => {
        console.log("Received stopProof");
        this.$store.commit('MUTATION_SET_FIND_PROOF', false);

      });
    } else{
        if(socket && socket.connected){
          socket.disconnect()
      }
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
