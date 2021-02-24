# Blockchain

## Get the current chain contents

> GET http://localhost/blockchain/chain

Required JSON:

```json
N / A
```

Example return:
Status code: 200

```json
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

Status code: 201

```json
{
  "success": true
}
```

or
Status code: 400

```json
{
  "err": "wallet ID already exists"
}
```

## Get Wallet Balance

> GET http://localhost/blockchain/wallet/balance

Required JSON:

```json
{
  "walletId": string
}
```

Example return:
Status code: 200

```json
{
  "amount": int
}
```

or
Status code: 400

```json
{
  "err": "no corresponding wallet for id"
}
```

## Verify transaction amount

POST http://localhost/blockchain/wallet/verifyAmount

Required JSON:

```json
{
  "walletId": string,
  "amount": int
}
```

Example return:

Status code: 200

```json
{
  "valid": true
}
```

or
Status code: 400

```json
{
  "err": "no corresponding wallet for id"
}
```
