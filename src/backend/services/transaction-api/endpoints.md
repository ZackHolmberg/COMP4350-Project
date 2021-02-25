# Transactions API

## Create a new Transaction

> `POST` <http://localhost/transactions/create>
> Required JSON:

```json
{
  "from": string,
  "to": string,
  "amount": float
}
```

- The from and to addresses are base64 encoded user key addresses, these will be used to verify the validity of the transaction
- The amount will need to be present in the users wallet to make a transaction

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
