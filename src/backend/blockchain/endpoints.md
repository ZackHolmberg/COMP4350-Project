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
  "umnetId": string
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
  "umnetId": string
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

## Create a new transaction

> `POST` <http://localhost/blockchain/wallet/createTransaction>

Required JSON:

```json
{
  "from": string,
  "amount": int,
  "to": string,
  "timestamp": int
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
  "error": string
}
```
