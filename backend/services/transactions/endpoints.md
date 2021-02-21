# Transactions API

## Generate keys for a user

> `POST` <http://localhost/transactions/keygen>

> Required JSON:

```json
{
  "user": string
}
```

Registers Private and Public keys for a User (temprorarily here, will be moved to User service in later iterations)\

Example return:

```json
{
  "success": boolean
}
```

## Get a public address for the user

> `GET` <http://localhost/transactions/username>

Example return:

```json
{
  "address": string
}
```

## Sign a message from a users private key

> `POST` <http://localhost/transactions/sign>

> Required JSON:

```json
{
  "to_sign": string,
  "user": string
}
```

Example return:

```json
{
  "to_sign": string,
  "signature": string
}
```

## Create a new Transaction

> `POST` <http://localhost/transactions/create>

> Required JSON:

```json
{
  "id": string,
  "from": string,
  "to": string,
  "amount": float,
  "signature": string
}
```

Example return:

```json
{
  "success": boolean
}
```
