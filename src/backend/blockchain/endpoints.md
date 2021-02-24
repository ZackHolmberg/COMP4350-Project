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
N / A
```

Example return:

```json
200

{
<<<<<<< HEAD
  "length": 1,
  "chain":
}
```

## Create a new wallet

> # `POST` <http://localhost/blockchain/wallet/addWallet>
>
> "amount": int
> }

````

or
Status code: 400

```json
{
  "err": "no corresponding wallet for id"
}
````

## Verify transaction amount

POST http://localhost/blockchain/wallet/verifyAmount

> > > > > > > master

Required JSON:

```json
{
<<<<<<< HEAD
  "walletId": string
=======
  "walletId": string,
  "amount": int
>>>>>>> master
}
```

Example return:

Status code: 200

```json
201

{
<<<<<<< HEAD
  "success": true
=======
  "valid": true
>>>>>>> master
}
```

or
<<<<<<< HEAD
=======
Status code: 400

> > > > > > > master

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
