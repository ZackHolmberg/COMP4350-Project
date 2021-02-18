# Blockchain API

## View the current contents of the chain

> `GET` <http://localhost/blockchain/chain>

Required JSON: `None`

Example return:

```json

```

## Start a new mining session for the provided transaction

> `POST` <http://localhost/blockchain/mine>

Required JSON:

```json
{ "toAddress": string, "fromAddress": string, "amount": int }
```

Example return:

```json

```

## Send a proof to the blockchain for the current mining session

> `POST` <http://localhost/blockchain/proof>

Required JSON:

```json
{ "proof": string }
```

Example return:

```json

```

## Register a new Wallet on the blockchain

> `POST` <http://localhost/blockchain/wallet/addWallet>

Required JSON:

```json
{ "walletId": string }
```

Example return:

```json

```

## Add an amount to a Wallet

> `POST` <http://localhost/blockchain/wallet/addAmount>

Required JSON:

```json
{ "walletId": string, "amount": int }
```

Example return:

```json
{ "newAmount": int }
```

## Subtract Amount from a Wallet

> `POST` <http://localhost/blockchain/wallet/subtractAmount>

Required JSON:

```json
{ "walletId": string, "amount": int }
```

Example return:

```json
{ "newAmount": int }
```

## Get a Wallet's current balance

> `GET` <http://localhost/blockchain/wallet/balance>

Required JSON:

```json
{ "walletId": string }
```

Example return:

```json
{ "amount": int }
```
