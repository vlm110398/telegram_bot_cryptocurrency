import json
import urllib.request
import time
import telepot
import csv
import datetime
bot_outputs = [] #bot output
delay = 20 #delay const
messages = [] #bot input
def push_binance(market_pair_coins): # get value of pair coin from binance api
  market_pair_coins = market_pair_coins.replace("/", "") #removing '/' ex: ETH/BTC => ETHBTC
  url = 'https://www.binance.com/api/v3/ticker/price'
  data =  json.load(urllib.request.urlopen(url))
  time.sleep(3)
  for x in data:
    if(x["symbol"] == market_pair_coins):  
        return float(x["price"])
  return -1  
def get_now_date():
    now = datetime.datetime.now()
    now = str(now.day) + '/' + str(now.month) + '/' + str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    return now

def push_bittrex(market_pair_coins): # get value of pair coin from bittrex api
    market_pair_coins = market_pair_coins.replace("/", "-")
    url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
    data =  json.load(urllib.request.urlopen(url))
    time.sleep(3)
    for x in data['result']:
        if(x['MarketName'] == market_pair_coins):
            return float(x['Ask'])
    return -1

def push_bitfinex(market_pair_coins): # get value of pair coin from bitfinex api
    market_pair_coins = market_pair_coins.replace("/", "")
    url = 'https://api.bitfinex.com/v2/tickers?symbols=t' + market_pair_coins
    data =  json.load(urllib.request.urlopen(url))
    time.sleep(3)
    if(data == []):
        return float(-1)   
    else:
        return (float(data[0][3]))  

def catch_message(msg): #bot catchs a user message
    if(msg['text'] == '!deletelast'): #command for delete a last message with a target and stop 
        messages.pop()
        bot_outputs.clear()
    elif(msg['text'] == '!deleteall'): #command for delete a all messages with a target and stop
        messages.clear()
        bot_outputs.clear()
    elif(msg['text'].find('!delay ') != -1): #command for change a delay const
        if(msg['text'][msg['text'].find('!delay ') + len('!delay ') : ].isdigit()):
            global delay
            delay = int(msg['text'][msg['text'].find('!delay ') + len('!delay '): ])
    elif(msg['text'].find('!submitcsv') != -1): #sends the csv relatory
        with open('relatory.csv', 'r', newline='') as csvfile:
            bot.sendDocument(-289210935, csvfile)
    elif(msg['text'].find('!newcsv') != -1): #blank the csv and create a new
        create_csv()    
    else: #if is not a command but is a target/stop message
        if(msg['text'].count('\n') >= 5):     
            messages.append(msg['text'])

def create_csv():
    with open('relatory.csv', 'w', newline='') as csvfile:
        return 0
def check_text(message_text):
    #target_price_list = []  #all target price of a message
    bot_response = "" #my aux bot_output var
    market_pair_coins = ""  # example : BTC/ETH
    max_price = -1    # max price from all exchanges
    buy_price = ""    # buy price in the message
    price_target_x = ""
    is_new = True # if this message is new
    print(message_text)
    i = 0
    for i in range(0,len(bot_outputs)): # walks in all bot outputs
        if(bot_outputs[i][ : bot_outputs[i].find('\n')] == message_text[ : message_text.find('\n')]): #if the begin is equal
            bot_response = bot_outputs[i] # 
            is_new = False #is not new message
            break
    if(is_new):
        bot_response = message_text
    position_espace = bot_response.find(' ')  #find the first espace  
    if(position_espace != -1 and position_espace != len(bot_response) -1): #if find the espace in not last index
        market_pair_coins = bot_response[      :  position_espace  ] #catch a coin name in the text
        #print(market_pair_coins)
    exchange = bot_response[position_espace + 1 : ]  #catch a exchange name and the remaining of text
    position_espace = exchange.find(' ')
    #print(position_espace)
    #print(exchange)
    date = exchange[ len(exchange) + 1: exchange.find('\n')] #take the date after the exchange
    exchange = exchange[ : position_espace] # ignore all after exchange name (remaining of text) 
    #print(exchange)
    
    buy_price = bot_response[ bot_response.find('BUY:') + len('BUY: ') :] #get a buy price in the text and the remaining of text
    buy_price = float(buy_price[ : buy_price.find('\n')])  #ignore remaining of text
    #print(buy_price)
    if(exchange): #this if is optional
      #print( str(push_bittrex(market_pair_coins)) + "\n" + str(push_binance(market_pair_coins)) + "\n" + str(push_bitfinex(market_pair_coins)) + "\n")
      #print( str(type(push_bittrex(market_pair_coins))) + "\n" + str(type(push_binance(market_pair_coins))) + "\n" + str(type(push_bitfinex(market_pair_coins))) + "\n")
      max_price = max([           #catch the max price of the 3 exchange
      push_bittrex(market_pair_coins),
      push_binance(market_pair_coins),
      push_bitfinex(market_pair_coins)
      ])
      print(max_price)
    position_stop_loss = bot_response.find('STOP LOSS:') #find the 'STOP LOSS:'
    stop_loss = bot_response[position_stop_loss :  ]  #take the string 'STOP LOSS:' with the position
    stop_loss_price = stop_loss[stop_loss.find(': ') + 2 : ] #take the price of stop loss
    number_target = 1  # start a counting
    while(True):               
        position_target_x = bot_response.find('TARGET' + str(number_target)+ '') #find a 'TARGET X:'
        if(position_target_x == -1):   
            break
        first_new_line = bot_response[position_target_x : ].find('\n') #separe TARGETS until a new line 
        target_x = bot_response[position_target_x :  position_target_x + first_new_line] #take a target x, separated on /n 
        position_target_x_price = position_target_x + len('TARGET') +len(str(number_target)) + 2 # catch the price position after 'TARGET X: ', 2 is ':' + ' '
        #print(str(position_target_x_price) + '\n')
        price_target_x = bot_response[position_target_x_price : position_target_x_price + bot_response[position_target_x_price :  ].find('\n')] #catch the price of 'TARGET X:'
        
        if(target_x.count((b'\xE2\x9C\x85').decode('utf-8'))):
          is_new = False
        elif(max_price != -1 and float(price_target_x) < max_price): #if max_price is -1, so nothing exchange uses this pair coins.  
            bot_response = bot_response[ : bot_response.find(price_target_x) + len(price_target_x)  ] + (b'\xE2\x9C\x85').decode('utf-8') + '(' + str(max_price) + ')'  +  str( format( ( (max_price/buy_price)-1)*100, '.2f' ) ) + '%' +  bot_response[ bot_response.find(price_target_x) + len(price_target_x) :  ] 
            with open('relatory.csv', 'a', newline='') as csvfile:
                fieldnames = [ 'date', 'paircoins', 'target', 'exchangeprice', 'buyprice', 'percent','stoploss', 'type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'date': get_now_date(), 'paircoins': str(market_pair_coins), 'target': str(price_target_x), 'exchangeprice' : str(max_price), 'buyprice' : str(buy_price), 'percent' :  str( format( ( (max_price/buy_price)-1)*100, '.2f' ) ) + '%' , 'stoploss' : str(stop_loss_price), 'type': 'target'})
            is_new = True
        number_target += 1 #X++
        
    
    #print(stop_loss)
    print(str(stop_loss_price) + "  " + str(max_price) + ' ' + 'BINANCE:' + str(push_binance(market_pair_coins)) + ' ' + 'BITTREX:'+ str(push_bittrex(market_pair_coins)) + ' ' + 'BITFINEX: ' + str(push_bitfinex(market_pair_coins)))
    if(stop_loss_price.replace('.','',1).isdigit()  and max_price != -1 and float(stop_loss_price) >= float(max_price)): #if the coin was stopped
        with open('relatory.csv', 'a', newline='') as csvfile:
            fieldnames = [ 'date', 'paircoins', 'target', 'exchangeprice', 'buyprice', 'percent','stoploss', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'date': get_now_date(), 'paircoins': str(market_pair_coins), 'target': str(price_target_x), 'exchangeprice' : str(max_price), 'buyprice' : str(buy_price), 'percent' :  str( format( ( (max_price/buy_price)-1)*100, '.2f' ) ) + '%' , 'stoploss' : str(stop_loss_price), 'type': 'stop'})
        is_new = True
        bot_response = bot_response[ : bot_response.find('STOP LOSS: ' + stop_loss_price) + len('STOP LOSS: ') +len(stop_loss_price)] + (b'\xE2\x9D\x8C').decode('utf-8') + bot_response[bot_response.find('STOP LOSS: ' + stop_loss_price) + len('STOP LOSS: ') +len(stop_loss_price) : ] 
    if(len(bot_outputs) != 0): #if bot_outputs is not empty
        i = 0
        for i in range(0,len(bot_outputs)): # walks in all bot outputs
            if(bot_outputs[i][ : bot_outputs[i].find('\n')] == bot_response[ : bot_response.find('\n')]): #if begin string is equal (first \n)
                if(bot_response.count((b'\xE2\x9D\x8C').decode('utf-8')) == 1 or bot_response.count((b'\xE2\x9C\x85').decode('utf-8')) == number_target):  #if is stopped or target count is equal
                    bot_outputs.remove(bot_outputs[i]) #delete this output
                    messages.remove(messages[i]) 
                elif(bot_response.count((b'\xE2\x9C\x85').decode('utf-8')) != bot_outputs[i].count((b'\xE2\x9C\x85').decode('utf-8'))):
                    bot_outputs[i] = bot_response     
                #if(len(bot_outputs)):      
                #    bot.sendMessage(-289210935, bot_response)
                #print('1')
    if(is_new):
        bot.sendMessage(-289210935, bot_response)    
        bot_outputs.append(bot_response)

bot = telepot.Bot("484373034:AAGuXOveFVQd4tbd46GXIKgFsuFUdpZ2hg4")
#print(bot.getUpdates())
create_csv()
bot.message_loop(catch_message)

while True:
    time.sleep(delay)
    #print(str(delay))
    for message in messages:
        check_text(message)
    print(bot_outputs)
    print(messages)
    pass