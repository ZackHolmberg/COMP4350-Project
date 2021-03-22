# Wallet API

## Get the user's wallet amount

> `POST` <http://localhost/wallet/amount>

**Required JSON:**

```json 
{
  "walletId": string
}
```
Returns the amount of bisoncoin that the user currently owns.

**Example return:**

```json
{
  "amount": int
}
```
or
```json
{
  "error" : string
}
```

## Get the user's transaction history

> `GET` <http://localhost/wallet/history?walletId={SearchID}>

Returns the transaction history of the wallet ID passed in the query.

*note: the mining rewards are formatted as transactions recieved from 'Mining'*

**Example return:**

```json
{
  "history": List of dicts arranged by timestamps by recency as follows 
  [
    {"timestamp": float, "from": string, "amount": float},
    {"timestamp": float, "to": string, "amount": float}
  ]
}
200
```
or
```json
{
  "error": "Please send correct json payload"
}
400
```
