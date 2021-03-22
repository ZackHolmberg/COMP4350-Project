# Wallet API

## Create a new wallet for a user

> `POST` <http://localhost/wallet/create>

**Required JSON:**

```json
{
  "walletId": string
}
```

Registers a wallet for a new user in the blockchain and returns the server message.

**Example return:**

```json
201 
{
  "success": boolean
}
```
or
```json
400 
{
  "error"  : string
}
```

## Get the user's wallet amount

> `POST` <http://localhost/wallet/amount>

**Required JSON:**

```json
200 
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
