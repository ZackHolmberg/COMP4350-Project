# Transactions API

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

- In the request the id needs to be a something that was signed by the users private key on the device
- signature is a base64 signature that was received from sigining the id
- The from and to addresses are base64 encoded public key addresses, these will be used to verify the validity of the transaction
- The amount will need to be present in the users wallet to maka a transaction

Example return:

```json
{
  "success": boolean
}
```

On a Bad request: 400

```json
{
  "err": string
}
```
