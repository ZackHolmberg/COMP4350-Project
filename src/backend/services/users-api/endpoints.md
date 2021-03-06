**IMPLEMENTED ENDPOINTS**: (please refer to user routes for returns):

- users/list(GET): returns a list of users present in the database

    **response**:

    {
        status = True
        data = [
            {
                first_name : string
                last_name : string
                umnetID : string
                public_key : string
            }
        ]
    }

    -or-

    failure payload with err in json file

- users/create(POST): add the user to the database, all the payload fields are required, returns an acknowledgment string

    **payload**: 
    
    {
        "first_name" : string
        "last_name" : string
        "umnetID" : string (UMNETID), unique
        "public_key" : string, unique
        "password" : string
    }

    **response**:

    {
        status : True
        message : 'user {firstname} {lastname} added successfully! :)'
    }

    -or-

    failure payload with err


- users/umnetID/<umnetID>(GET): returns the info of a particular user. 

    **response**:

    {
        status : True
        data : {
            first_name : string
            last_name : string
            umnetID : string
            public_key : string
        }
    }

    -or-

    failure payload with data : error messafe

- users/login (POST): returns true if login is successful else false

    **payload**: {
        "umnetID": string
        "password" : string
    } 

    **response**:

    {
        success : True
    }

    -or-

    failure payload with err

- users/update (POST): updates the user's info. CANNOT UPDATE UMNETID

    **payload**: {
         "first_name": string
         "last_name": string
         "curr_password": string (used for verification)
         "new_password": string (same as old password if you don't wanna change the password)
         "umnetID": string
         "public_key": string
    }

    **response**:

    {
        status = True
        message = 'user {umnetID} updated successfully! :)'
    }

    -or-

    failure payload with error message in "err:"