#to get api_key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')

#creating a new bot
import telebot 
bot=telebot.TeleBot(api_key,parse_mode=None)


#for ML model 
import pickle
import pandas as pd

# get the model saved earlier
model = pickle.load(open("Diabetes.pkl", "rb"))  ##loading model


#this command makes the bot to send a message as a reply 
@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message,"Hey , Hello and welcome to the diabetes prediction bot. We are delighted to assist you. To obtain the prognosis, please enter the following command"+ 
    '\n\n\n Predict-<No of pregnancies>-<Glucose Level>-<Blood Pressure>-<Skin Thickness>-<BMI>-<Insulin Level>-<Diabetes Pedigree Function>-<Age> \n\n'+
    "Replace each variable with its corresponding reading using command. To obtain the forecast")



#this message doesn't appear as a reply but as an indivisual and standalone message 
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"Kindly Contact @nishantkumarrr to report any bugs and suggestions.Thank you :-)")


#predict function starts

#validation function to validate the entries
def prediction_request(message):
    variables= message.text.split("-")
    if len(variables)<9 :
        print("na na na na ")
        return False
    else:
        return True
    
#here instead of cheaking the basic command it check for validation using the function provided by user
@bot.message_handler(func=prediction_request)
def send_outcome(message):
        variables= message.text.split("-")
        print(variables)
        variables.pop(0)
        print(variables)
        row_df =  pd.DataFrame([pd.Series(variables)])
        print(type(row_df))
        prediction=model.predict_proba(row_df) 
        output='{0:.{1}f}'.format(prediction[0][1], 2)    ## Formating output
        if output>str(0.5):
            pred='You have certain diabetes symptoms. Please contact a doctor for a more personalised diagnosis. Take precautions.'
        else:
            pred='Hurray ! You are safe. You have no diabetes symptoms. Have a nice day'
        bot.send_message(message.chat.id,pred)



#to check constantly if this any new message is being given to bot
bot.infinity_polling()
