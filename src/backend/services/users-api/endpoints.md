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
      "umnetID": string,
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
  "umnetID": string,
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

> users/umnetID/{{umnetID}}(GET): returns the info of a particular user.

### Response

```json
{
  "success": true,
  "data": {
    "first_name": string,
    "last_name": string,
    "umnetID": string,
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
  "umnetID": string,
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

## Update User

> users/update (POST): updates the user's info. CANNOT UPDATE UMNETID

### Payload

```json
{
"first_name": string,
"last_name": string,
"curr_password": string (used for verification),
"new_password": string (same as old password if you don't wanna change the password),
"umnetID": string,
"public_key": string,
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