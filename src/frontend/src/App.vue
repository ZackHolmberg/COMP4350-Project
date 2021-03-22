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

  get umnetId(){
    return this.$store.getters.umnetId
  }

  get findProof(){
    return this.$store.getters.findProof
  }

  validHash (hash: string): boolean  {
      return hash.startsWith("0000", 0);
  }

  computeHash(nonce: number, transaction: Transaction): string {
      const toHash = ( nonce.toString() + transaction.amount.toString() + transaction.timestamp.toString() + transaction.id + transaction.signature ).replace(/(\r\n|\n|\r)/gm, "");
      return sha256(toHash);
  }

  proofOfWork(transaction: Transaction): any  {
      let nonce = -1;
      let hash = "";
      while (!this.validHash(hash) && this.findProof) {
        nonce += 1;
        hash = this.computeHash(nonce, transaction);
      }
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
        socket.on("findProof", (...args: any) => {
        this.$store.dispatch("ACTION_DISPLAY_TOAST", { message: 'Mining session unsuccesful', type: 'success' })
        this.$store.commit('MUTATION_SET_FIND_PROOF', true);

        const transaction: Transaction = {
          "to": args[0].to,
          "from": args[0].from,
          "amount": parseFloat(args[0].amount),
          "timestamp": parseInt(args[0].timestamp),
          "id": args[0].id,
          "signature": args[0].signature,
        };
        const temp = this.proofOfWork(transaction);

        if(this.validHash(temp.proof)){
          const toSend = {
            "proof":temp.proof,
            "nonce":temp.nonce,
            "id": transaction.id,
            "minerId": this.umnetId
          }

          socket.emit("proof",toSend)
          this.$store.commit('MUTATION_SET_FIND_PROOF', false);

        }
      });

      socket.on("reward", () => {
          this.$store.dispatch("ACTION_FETCH_WALLET_AMOUNT");
          this.$store.dispatch("ACTION_DISPLAY_TOAST", { message: 'Mining reward received!', type: 'success' })

      });

      socket.on("stopProof", () => {
        if(this.findProof){
          this.$store.commit('MUTATION_SET_FIND_PROOF', false);
          this.$store.dispatch("ACTION_DISPLAY_TOAST", { message: 'Mining session unsuccesful', type: 'warning' })
        }
      });
      }
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
