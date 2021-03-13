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

  validHash (hash: string): boolean  {
      return hash.startsWith("0000", 0);
  }

  computeHash(nonce: number, transaction: Transaction): string {
      return sha256(
        nonce.toString() + transaction.to + transaction.from + transaction.amount.toString() + transaction.id + transaction.signature
      );
  }

  proofOfWork(transaction: Transaction): string  {
      let nonce = 0;
      let hash = "";
      while (!this.validHash(hash) && this.$store.getters.mining) {
        hash = this.computeHash(nonce, transaction);
        nonce += 1;
      }

      return hash;
  }

  get mining() {
    const mining = this.$store.getters.mining;
    if (mining) {
      socket.on("findProof", (...args: any) => {
        const transaction: Transaction = {
        "to": args.to,
        "from": args.from,
        "amount": parseFloat(args.transaction.amount),
        "id": args.transaction.id,
        "signature": args.transaction.signature,
        };

        const hash = this.proofOfWork(transaction);

        if(this.validHash(hash)){
          const toSend = {

          }
            socket.emit("proof",hash)
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
