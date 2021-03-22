# User API

## List Users

> users/list(GET): returns a list of users present in the database

### Response

```json
{
  "success": true,
  "data": [
    {
      "first_name": string,
      "last_name": string,
      "umnetId": string,
      "public_key": string
    },
    ...
  ]
}
```

-or-

```json
{ "error": string }
```

## Create User

> users/create(POST): add the user to the database, all the payload fields are required, returns an acknowledgment string

### Payload

```json
{
  "first_name": string,
  "last_name": string,
  "umnetId": string,
  "public_key": string,
  "password": string
}
```

### Response

```json
{ "success": true }
```

-or-

```json
{ "error": string }
```

## Get User

> users/umnetId/{{umnetId}}(GET): returns the info of a particular user.

### Response

```json
{
  "success": true,
  "data": {
    "first_name": string,
    "last_name": string,
    "umnetId": string,
    "public_key": string
  }
}
```

-or-

```json
{ "error": string }
```

## Login

> users/login (POST): returns true if login is successful else false

### Payload

```json
{
  "umnetId": string,
  "password": string
}
```

### Response

```json
{
  "first_name": string,
  "last_name": string,
  "public_key": string
}
```

-or-

```json
{ "error": string }
```

## Update User

> users/update (POST): updates the user's info. CANNOT UPDATE UMNETID

### Payload

```json
{
  "first_name": string,
  "last_name": string,
  "umnetId": string,
  "public_key": string,
  "curr_password": string,
  "new_password": string
}
```

### Response

```json
{ "success": true }
```

-or-

```json
{ "error": string }
```
