# Transactions API

## Create a new Transaction

> `POST` <http://localhost/transactions/create>
> Required JSON:

```json
{
  "id": string,
  "from": string,
  "to": string,
  "timestamp": int,
  "amount": float,
  "signature": float
}
```

- The from and to addresses are encoded user key addresses, these will be used to verify the validity of the transaction
- The amount will need to be present in the users wallet to make a transaction
- id is a random transaction id that will be signed with the private key
- Signature is the signed transaction id from the private key of the public key address
- Timestamp represents the epoch time in seconds when the transaction was created by the user

Example return:

```json
{
  "success": boolean,
  "remaining_amount": float
}
```

On a Bad request: 400

```json
{
  "err": string
}
```
