from .models import ResetToken
from django.contrib.auth.models import User
from dotenv import load_dotenv
import os
import random
import math
import yagmail


load_dotenv()
randit = str(math.floor(random.random() * 7652196 + 1))
value = int(randit[0:5])
otp = value
port = 465

sender = os.getenv("SENDER")
password = os.getenv("PASSWORD")

# function to generate otp code
def send_token(email,name):
    msg = """\
    hello {0},
    To reset your hyper account, please use the following OTP:

    {1}

    regards

    Mozzie
    """.format(name,otp)
    yag = yagmail.SMTP(sender, password)
    yag.send(email, 'Reset Token', msg)
    print("mail successfully sent")
    user = User.objects.get(username=name)
    ResetToken.objects.create(user=user,token=otp)

