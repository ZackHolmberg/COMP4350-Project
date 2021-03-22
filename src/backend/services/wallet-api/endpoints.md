# Wallet API

## Create a new wallet for a user

> `POST` <http://localhost/wallet/create>

**Required JSON:**

```json
{
  "umnetId": string
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
  "umnetId": string
}
```

Returns the amount of bisoncoin that the user currently owns.

**Example return:**

```json
400
{
  "amount": int
}
```

or

```json
{
  "error": string
}
```
