# Blockchain API

## View the current contents of the chain

> `GET` <http://localhost/blockchain/chain>

Required JSON: `None`

Example return:

```json
{
  "length": 1,
  "chain": [
    {
      "hash": "0000",
      "index": 0,
      "nonce": 0,
      "prev_hash": "0",
      "timestamp": "1614063326.48",
      "transaction": { "amount": 0, "from_address": "", "to_address": "" }
    }
  ]
}
```

## Send a proof to the blockchain for the current mining session

> `POST` <http://localhost/blockchain/proof>

Required JSON:

```json
{ "proof": string }
```

Example return:

```json
TBD
```

## Register a new Wallet on the blockchain

> `POST` <http://localhost/blockchain/wallet/addWallet>

Required JSON:

```json
{ "walletId": string }
```

Example return:

```json
200 { "success": true }
```

or

```json
400 {"error": "wallet ID already exists"}
```

## Verify that a wallet has sufficient funds for the transaction

> `POST` <http://localhost/blockchain/wallet/verifyAmount>

Required JSON:

```json
{ "walletId": string, "amount": int }
```

Example return:

```json
200 { "valid": true }
```

or

```json
200 { "valid": false }
```

depending whether or not the wallet has sufficient funds greater than or equal to `amount`.

## Get a Wallet's current balance

> `GET` <http://localhost/blockchain/wallet/balance>

Required JSON:

```json
{ "walletId": string }
```

Example return:

```json
200 { "amount": int }
```

or

```json
400 { "error": "no corresponding wallet for id" }
```
