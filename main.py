import os
import requests
import telebot

from time import sleep
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions


def sendTelegramAlert(text, chat_id):
    bot = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))
    bot.send_message(chat_id, text, parse_mode="html")


def pushEventLogToDatabase(supabase, event):
    # Update to ensure the specific event information are added to the database
    supabase.table('TABLE NAME HERE').insert({
        "subject": event['args']['subject'],
        "transactionHash": Web3.to_hex(event['transactionHash']),  #TODO: explain web3 data class
        "blockNumber": event['blockNumber']
    }).execute()


#TODO: Create update database function


def log_loop(event_filter, poll_interval, ss):
    client_options = ClientOptions(postgrest_client_timeout=None, storage_client_timeout=None)
    supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"), options=client_options)

    setStartBlock = True
    while True:
        event_filter_entries = event_filter.get_new_entries()

        if ss:
            print(f'Executing Startup Process: {ss}')

        if setStartBlock and len(event_filter_entries) != 0:
            upperblock = event_filter_entries[0]['blockNumber']
            print(f"Block Number: {upperblock}")
            setStartBlock = False

        print(f'Number of Entries: {len(event_filter_entries)}')
        for event in event_filter_entries:
            if ss:
                print('Processing block gap fill task...')
                # Upon restart the program will check the database and insert missed blocks
                #TODO: check all missing blocks for data
                # updateDatabaseOnStart(supabase, upperblock)

                ss = False
                print('Missing data has been inserted.')

            pushEventLogToDatabase(supabase, event)

        sleep(poll_interval)
    


def getEvents():
    startup_status = True

    # Initiates Web3 http object
    node_provider_api_key = os.environ.get('node_provider_api_key') 
    w3 = Web3(Web3.HTTPProvider(node_provider_api_key))

    # Load or get ABI
    with open("./contractABI.json", "r") as file:
        contractABI = file.read()

    # Contract Address
    contract_address = Web3.to_checksum_address('Enter Contract Address Here')

    # Creates contract object
    event_contract = w3.eth.contract(address=contract_address, abi=contractABI)

    # Creates filter 
    event_filter = event_contract.events.Trade.create_filter(fromBlock="latest")

    # Begins 
    log_loop(event_filter, 2, startup_status)

    return None


if __name__ == "__main__":
    try:
        # loads .env to environement 
        load_dotenv(override=True)

        # Sends Telegram Alert on start up
        sendTelegramAlert(f'Indexer has started: {datetime.now()}', "CHAT ID")

        # begins loop
        getEvents()

    finally:
        # Sends Telegram Alert on start up
        sendTelegramAlert(f'Indexer has shut down: {datetime.now()}', "CHAT ID")
        print(f'Indexer has shut down: {datetime.now()}')


