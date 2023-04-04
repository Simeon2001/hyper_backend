#   COMPAYM
 compaym is a fintech application to send and receive money using username tag and disbursting of money to family and friends even your worker using a form.

 ## FEATURES
 * send and receive money with username tag.
 * distribute money to family and friends with just one click by creating a form for family and friends to add their username tag.
 * with this form it can be use as a payroll to pay family member even worker, because when you collect the usernames using the form you can reuse the collected username to pay them next time.
 * you can also create a unique form to store account number and amount to be paid for each of your workers and pay them there salary with just one click.

## URL
 Frontend Url: https://hyper-beta.vercel.app

 ## TUTORIALS

* TO CREATE AN ACCOUNT USE http://127.0.0.1:8000/api/register then with a post request containing the json data:
--------------------

    {"username":"hartech","password":"Linktree2021","last_name":"jesusanya","first_name":"simeon""email":"hartech@gmail.com"}
-------------------------------------

after registering it automatically create an authtoken.

* TO LOGIN TO ACCOUNT USE http://127.0.0.1:8000/api/token then with a post request containing the json data:
--------------------

    {"username":"jesse","password":"Apple2020"}
-------------------------------------

* which generate this result:

--------------------

    {"status":true,"token":"121fe8dbc25140d8fa896a6367221acf55616891","profile_empty":false}
-------------------------------------

* TO CREATE PROFILE USE http://127.0.0.1:8000/api/create-profile then with a post request and user TOKEN containing the json data:
--------------------

    {"country":"Nigeria","account_number":"0450054410","account_name":"jesusanya simeon","bank_name":"GTB","mobile_number":"09036625937"}
-------------------------------------

* TO GET PROFILE DETAILS OF EACH USER USE http://127.0.0.1:8000/api/profile then with a GET request and user TOKEN with a result of this:
which contain 

--------------------

    {
    "user": "anon",
    "country": "usa",
    "currency": "dollar",
    "account_number": 450054410,
    "names": [
        {
            "balance": 90032009
        }
    ]
}
-------------------------------------

* TO GET BALANCE USE http://127.0.0.1:8000/api/bal then with a GET request with a result:
--------------------
    {"balance": 90032009}
-------------------------------------

* TO GET each user multiple pay form title and id USE http://127.0.0.1:8000/api/multi-info then with a GET request with a result:
--------------------
    {
    "id": [
        1,
        2
    ],
    "title": [
        "giveaway for buddies",
        "giveaway"]}
-------------------------------------

* TO create a new form to add user you want to share money to USE http://127.0.0.1:8000/api/multi-info then with a POST request and this:
* NOTE: closing_no is the number of user you want to share money to.
--------------------
    {"title": "money for foods for fam",
    "closing_no": "10"}
-------------------------------------

* TO add an username to a certain user form USE http://127.0.0.1:8000/api/multi-post/id then with a POST request, the id should be a number e.g id = 1 or 2 then 
--------------------
    {"username": "sim"}
-------------------------------------

* TO generate link to deposit money USE http://127.0.0.1:8000/api/link then with a POST request then with input :
--------------------
    {"amount": "5000"}
-------------------------------------

* TO send money using your username tag USE http://127.0.0.1:8000/api/trans with a POST request then with input :
--------------------
    {"amount": "5000","reason":"money for feeding","tag":"sim"}
-------------------------------------

* TO get the profile status either if it have been created or not USE http://127.0.0.1:8000/api/profile-status with a GET request with a response:
--------------------
    {"status":true,"user":"anon","profile_empty":false}
-------------------------------------

* TO get transcation notification USE http://127.0.0.1:8000/api/notify with a GET request with a response:
--------------------
    {
        "amount": 500,
        "send": "anon",
        "receive": "ciscoquan",
        "reason": "ass",
        "date_added": "2022-06-04T11:13:22.157200Z"
    },
    {
        "amount": 500,
        "send": "anon",
        "receive": "ciscoquan",
        "reason": "ass",
        "date_added": "2022-06-04T11:12:19.656326Z"
    },
    {
        "amount": 5000,
        "send": "anon",
        "receive": "ciscoquan",
        "reason": "ass",
        "date_added": "2022-06-04T11:11:36.675342Z"
    },
    {
        "amount": 5000,
        "send": "ciscoquan",
        "receive": "anon",
        "reason": "whatsapp transaction",
        "date_added": "2022-05-24T11:42:30.063191Z"
    }
-------------------------------------

* TO search for a user and confirm if it the user by their first and last name USE http://127.0.0.1:8000/api/search with a POST request with a data:
--------------------
    {"search":"sim"}

with a response:

    [
    {
        "first_name": "simi",
        "last_name": "simi",
        "username": "sim"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simv"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simc"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simu"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simo"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simb_q"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simbh"
    },
    {
        "first_name": "leke",
        "last_name": "owaj",
        "username": "simyb"
    }
    ]
    
-------------------------------------