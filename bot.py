
import mysql.connector
import datetime
from datetime import date
import calendar
from pytz import timezone

from aiogram.types import InlineKeyboardButton 
from aiogram import executor,Dispatcher,Bot,types
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
button1=InlineKeyboardButton(text="Reward",callback_data="reward")
inlinebtn=InlineKeyboardMarkup().add(button1)
# from tronapi import Tron
# from tronapi import HttpProvider
from web3 import Web3
import json
import config
import requests

import json

# Read configuration from the file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

#--------------------------
api_key=config["api_key"]
YOURPRIVATEKEY=config["YOURPRIVATEKEY"]
defaultAddress=config["defaultAddress"]  #add your default address here
CONTRACT_ADDRESS=config["CONTRACT_ADDRESS"]#add your contract address





#-----------------------------







#adding reward function 
def sendReward(reward_Count,address):
        
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    print(web3.isConnected())

    main_address= defaultAddress
    contract_address = CONTRACT_ADDRESS #be sure to use a BSC Address in uppercase format like this 0x9F0818B... 

    abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')

    contract = web3.eth.contract(address=contract_address, abi=abi)

    totalSupply = contract.functions.totalSupply().call()

    print(web3.fromWei(totalSupply, 'ether'))

    print(contract.functions.name().call())
    print(contract.functions.symbol().call())


    balanceOf = contract.functions.balanceOf(main_address).call()
    print(web3.fromWei(balanceOf, 'ether'))

    me = defaultAddress  #send from this address
    main_address=str(address)   #to this address

    send = 0.1*int(reward_Count)
    amount = web3.toWei(send, 'ether')
    print(amount)

    nonce = web3.eth.getTransactionCount(me)
    print(nonce)

    token_tx = contract.functions.transfer(main_address, amount).buildTransaction({
        'chainId':56, 'gas': 100000,'gasPrice': web3.toWei('10','gwei'), 'nonce':nonce
    })
    sign_txn = web3.eth.account.signTransaction(token_tx, private_key=YOURPRIVATEKEY)
    web3.eth.sendRawTransaction(sign_txn.rawTransaction)
    print(f"Transaction has been sent to {main_address}")

#ADDINGN THE API KEYS
bot_=Bot(token=api_key)
bot=Dispatcher(bot_)
username=""
mydb=mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        passwd=config["passwd"],
        database=config["database"]
    )
print("connected")
mycursor = mydb.cursor()

#CREATING SOME TABLES
try:
    mycursor.execute(f"CREATE TABLE `usersmessages` (userid VARCHAR(255),name VARCHAR(255), date VARCHAR(255), day VARCHAR(255))")
except:
    pass

try:
    mycursor.execute(f"CREATE TABLE `rewards` (userid VARCHAR(255),name VARCHAR(255), morning VARCHAR(255), night VARCHAR(255),date VARCHAR(255))")
except Exception as err:
  print(err)
    
try:   
    mycursor.execute(f"CREATE TABLE `address2` ( userid VARCHAR(255),Fname VARCHAR(255), Sname VARCHAR(255),username VARCHAR(255),address VARCHAR(255),time VARCHAR(255),date VARCHAR(255))")

except:
    pass



@bot.errors_handler()  # handle the cases when this exception raises 
async def message_not_modified_handler(update, error): 
     global mycursor,mydb
     mydb=mysql.connector.connect(
       host=config["host"],
        user=config["user"],
        passwd=config["passwd"],
        database=config["database"]
    )
     print("connected")
     mycursor = mydb.cursor()
     return True # errors_handler must return True if error was handled correctly     



#CREATING LINKS HERE


@bot.message_handler(commands=['createlink'])
async def greet(message:types.Message):
    print("creating link")
    print(message)
    chat_id=message['chat']['id']
    user_id=message['from']['id']
    # username=message['from']['username']
    r=requests.get(f"https://api.telegram.org/bot{api_key}/createChatInviteLink?chat_id={chat_id}")
    invitee=r.json()['result']['invite_link']
    #UPDATING DATABSAE

    mycursor.execute(f"SELECT address FROM `address2` WHERE username='{str(message['from']['username'])}'")
    result = mycursor.fetchall()
    print("messag")
    print(str(message['from']['username']))
    if(result==[]):
        mycursor.execute(f"INSERT INTO `inviteReward` ( `userid`,`name`, `link`) VALUES ('{str(user_id)}','{str(message['from']['username'])}','{str(invitee)}')")
        mydb.commit()
    
    await message.reply(f"your link is {invitee}")


###------------------->
@bot.message_handler(commands=['bsc'])
async def greet(message:types.Message):
        global username
        print(message)
        username=message['from']['username']
        await message.reply("Please enter the BSC wallet address to claim the reward token.")
@bot.message_handler(commands=['claim'])
async def greet(message:types.Message):
    await message.reply("'reward' Claim the token when the button is pressed..",reply_markup=inlinebtn)


###GIVING REWARD
def userInvitee(inviter):
    mycursor.execute(f"SELECT name,peoples FROM `inviteReward`")
    results = mycursor.fetchall()
    people_reward=""
    for result in results:
        if inviter in result[1].split(","):
            people_reward=result[0]
    
    print(people_reward)
    
    return people_reward

#####under construction please change everything properlyu
@bot.callback_query_handler(text=['reward'])
async def reward(message:types.Message):
    mycursor.execute(f"SELECT morning,night FROM `rewards` WHERE name='{str(message['from']['username'])}'")
    result = mycursor.fetchall()
    reward_Count=2
    #--->should change==
    # for i in result:
    #     if(int(i[0])>=1 and int(i[1])>=1):
    #         reward_Count+=1
    if(not(reward_Count==0)):
        mycursor.execute(f"SELECT address FROM `address2` WHERE username='{str(message['from']['username'])}'")
        result = mycursor.fetchall()
        if(not(result==[])):
            print(f"sending reward to {message['from']['username']}")
            # sendReward(reward_Count,result[0][0])
            #->shoudl change==
            ##
            invitation_Reward=userInvitee(str(message['from']['username']))
            print(invitation_Reward)
            if(invitation_Reward!=""):
                mycursor.execute(f"SELECT address FROM `address2` WHERE username='{invitation_Reward}'")
                result = mycursor.fetchall()
                if(not(result==[])):
                    #->shoudl change==
                    # sendReward(reward_Count,result[0][0])
                    print("working inside ")
                    print(f"sending reward to {invitation_Reward}")
            #-->


            await message.answer(f" {0.1*int(reward_Count)} Send reward tokens.")
            mycursor.execute(f"DELETE FROM rewards WHERE name='{str(message['from']['username'])}'")
            mydb.commit()
        else:
            
                await message.answer(f"/bsc After entering, register your BSC wallet address.")

    else:
        await message.answer(f"There are no tokens to be rewarded.")


  
@bot.message_handler()

async def echo_all(message:types.Message):
        global username
        Current_Date_Formatted = datetime.datetime.today().strftime ('%d-%m-%Y')
        dates_array=[]
        today = datetime.datetime.now(timezone('Asia/Seoul'))
        time_reward=today.strftime("%H")
        time=str(datetime.datetime.now().strftime("%H:%M:%S"))
        curr_date = today.strftime ('%d-%m-%Y')
        date_=str(curr_date)
        # day=calendar.day_name[curr_date.weekday()]
        if(message['from']['username']==username): 
            if("0"==str(message.text)[0].lower() and "x"==str(message.text)[1].lower()):
                await message.reply("BSC Your address has been registered.")
                mycursor.execute(f"SELECT address FROM `address2` WHERE username='{str(message['from']['username'])}'")
                result = mycursor.fetchall()
                
                if(result==[]):
                    mycursor.execute(f"INSERT INTO `address2` ( `Fname`, `Sname`,`username`,`address`,`time`,`date`) VALUES ('{str(message['from']['first_name'])}','{str(message['from']['last_name'])}','{message['from']['username']}','{str(message.text)}','{time}','{date_}')")
                    mydb.commit()
                    username=""


                else:
                    mycursor.execute(f"UPDATE `address2` SET address = '{str(message.text)}' WHERE username ='{message['from']['username']}'")
                    mydb.commit()
                    mycursor.execute(f"UPDATE `address2` SET time = '{str(time)}' WHERE username ='{message['from']['username']}'")
                    mydb.commit()
                    mycursor.execute(f"UPDATE `address2` SET date = '{str(date_)}' WHERE username ='{message['from']['username']}'")
                    mydb.commit()
                    username=""
                    

            else:
                await message.reply("BSC 지갑 주소를 확인 후 등록해주세요.")
            username=""
            

        else:
            morning=["06","07","08","09","10","11","12","13","14","15"]
            night=['18','19','20','21','22','23','24','00','01',"02","03"]
            if(time_reward in morning):
                if("모닝" in str(message.text)):
                    print("saving mesag morning")

                    mycursor.execute(f"SELECT morning FROM `rewards` WHERE name='{str(message['from']['username'])}' AND date='{str(date_)}'")
                    result = mycursor.fetchall()
                    if(result==[]):
                        mycursor.execute(f"INSERT INTO `rewards` ( `name`, `morning`,`night`,`date`) VALUES ('{str(message['from']['username'])}','1','0','{date_}')")
                        mydb.commit()
                    else:
                        mycursor.execute(f"UPDATE `rewards` SET morning = '{int(result[0][0])+1}' WHERE name ='{message['from']['username']}'  AND date='{str(date_)}'")
                        mydb.commit()
            if(time_reward in night):
                if("나잇" in str(message.text)):
                    print("saving mesag night")
                    mycursor.execute(f"SELECT night FROM `rewards` WHERE name='{str(message['from']['username'])}' AND date='{str(date_)}'")
                    result = mycursor.fetchall()
                    if(result==[]):
                        mycursor.execute(f"INSERT INTO `rewards` ( `name`, `morning`,`night`,`date`) VALUES ('{str(message['from']['username'])}','0','1','{date_}')")
                        mydb.commit()
                    else:
                        mycursor.execute(f"UPDATE `rewards` SET night = '{int(result[0][0])+1}' WHERE name ='{message['from']['username']}'  AND date='{str(date_)}'")
                        mydb.commit()
                    



  





    


executor.start_polling(bot)

