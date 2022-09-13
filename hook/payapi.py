import requests
from requests.structures import CaseInsensitiveDict
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.getenv("API_KEY")
headers = CaseInsensitiveDict()

headers["Content-Type"] = "application/json"
headers["Authorization"] = "Bearer {0}".format(api_token)

# to generate link to deposit cash
def charge(em, am):

    p_url = "https://api.paystack.co/transaction/initialize"
    info = {"email": em, "amount": am}
    data = json.dumps(info, indent=2)

    res = requests.post(p_url, headers=headers, data=data)
    v = res.json()
    return v


# total transcation done on account
def total_transcation():
    p_url = "https://api.paystack.co/transaction/totals"
    res = requests.get(p_url, headers=headers)
    v = res.json()
    return v


# get account balance
def balance():
    p_url = "https://api.paystack.co/balance"
    res = requests.get(p_url, headers=headers)
    v = res.json()
    return v


# create customer
def customer(em, first_name, last_name, phone):
    p_url = "https://api.paystack.co/customer"
    info = {
        "email": em,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
    }
    data = json.dumps(info, indent=2)

    res = requests.post(p_url, headers=headers, data=data)
    v = res.json()
    return v


# validate your customer using their bvn
def validate_customer(customer_code, value, first_name, last_name):
    p_url = "https://api.paystack.co/customer/{0}/identification".format(customer_code)
    info = {
        "country": "NG",
        "type": "bvn",
        "value": value,
        "first_name": first_name,
        "last_name": last_name,
    }
    data = json.dumps(info, indent=2)

    res = requests.post(p_url, headers=headers, data=data)
    v = res.json()
    return v


# create account number for customer
def nuban(customer_id):
    p_url = "https://api.paystack.co/dedicated_account"
    info = {"customer": customer_id, "preferred_bank": "wema-bank"}
    data = json.dumps(info, indent=2)

    res = requests.post(p_url, headers=headers, data=data)
    v = res.json()
    return v


# generate authorization code for transfer
def transfer_code(name, account_no, bank_code):
    p_url = "https://api.paystack.co/transferrecipient"
    info = {
        "type": "nuban",
        "name": name,
        "description": "your compaym account",
        "account_number": str(account_no),
        "bank_code": bank_code,
        "currency": "NGN",
    }
    res = requests.post(p_url, headers=headers, data=info)
    v = res
    return v


# transfer funds from your balance to customer account
def transfer_cash(recipient_code, amount):
    p_url = "https://api.paystack.co/transfer"
    info = {
        "source": "balance",
        "reason": "payment from compaym",
        "recipient": recipient_code,
        "amount": amount,
    }
    res = requests.post(p_url, headers=headers, data=info)
    v = res
    return v


# to check if transfer was successful or not
def verify_transfer(reference):
    p_url = "https://api.paystack.co/transfer/verify/{0}".format(reference)
    res = requests.get(p_url, headers=headers)
    v = res.json()
    return v


# retrieve part of a payment from a customer
def partial_debit(author_code, currency, amount, email):
    p_url = "https://api.paystack.co/transaction/partial_debit"
    info = {
        "authorization_code": author_code,
        "currency": currency,
        "amount": amount,
        "email": email,
    }
    res = requests.post(p_url, headers=headers, data=info)
    v = res
    return v


# this allow you to create and manage installment payment option
def create_plan(name, amount, interval):
    p_url = "https://api.paystack.co/plan"
    info = {"name": name, "interval": interval, "amount": amount}
    res = requests.post(p_url, headers=headers, data=info)
    v = res
    return v


# allows you to manage recurring payment
def create_subscription(customer_code, plan_code):
    p_url = "https://api.paystack.co/subscription"
    info = {"customer": customer_code, "plan": plan_code}
    res = requests.post(p_url, headers=headers, data=info)
    v = res
    return v


# enable subscription
def enable_subscription(subscription_code, token):
    p_url = "https://api.paystack.co/subscription/token"
    info = {"code": subscription_code, "token": token}
    res = requests.post(p_url, headers=headers, data=info)
    v = res
    return v


# disable otp for transfer
def disable_otp():
    p_url = "https://api.paystack.co/transfer/disable_otp"
    res = requests.post(p_url, headers=headers)
    v = res
    return v


def enable_otp():
    p_url = "https://api.paystack.co/transfer/enable_otp"
    res = requests.post(p_url, headers=headers)
    v = res
    return v
