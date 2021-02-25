# Blockchain

## Get the current chain contents

> GET http://localhost/blockchain/chain

Required JSON:

```json
N / A
```

Example return:

```json
200

{
  "length": 1,
  "chain":
}
```

## Create a new wallet

> POST http://localhost/blockchain/wallet/addWallet

Required JSON:

```json
{
  "walletId": string
}
```

Example return:


```json
200

{
  "success": true
}
```
or

```json
400

{
  "err": "wallet ID already exists"
}
```

## Get Wallet Balance

> `GET` <http://localhost/blockchain/wallet/balance>

Required JSON:

```json
{
  "walletId": string
}
```

Example return:

```json
200

{
  "amount": int
}
```

or

```json
400

{
  "err": "no corresponding wallet for id"
}
```

## Verify transaction amount

> `POST` <http://localhost/blockchain/wallet/verifyAmount>

Required JSON:

```json
{
  "walletId": string,
  "amount": int
}
```

Example return:

```json
200

{
  "valid": true
}
```

or

```json
400

{
  "err": "no corresponding wallet for id"
}
```
