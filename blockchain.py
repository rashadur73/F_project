from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict
import pickle

from hash_util import hash_string_256,hash_block


MINING_REWARD = 10
#genesis block removed
blockchain = []
open_transactions = []
owner = 'Rashadur'
participants = {'Rashadur'}

def load_data():
    global blockchain
    global open_transactions

    try :
        with open('blockchain.txt',mode = 'r') as f:
            #for pickle --------------------------
            # file_content = pickle.loads(f.read())
            # print(file_content)
            # global blockchain
            # global open_transactions
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            #blockchain = [{'previous_hash':block['previous_hash'], 'index' : block['index'], 'proof' : block['proof'],'transactions': []} for block in blockchain]
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                    'previous_hash':block['previous_hash'],
                    'index' : block['index'],
                    'proof' : block['proof'],
                    'transactions' : [OrderedDict([('sender',tx['sender']), ('recipient' ,tx['recipient']), ('amount',tx['amount'])]) for tx in block['transactions']]
                } 
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            updated_open_transactions = []
            for tx in open_transactions:
                updated_tx = OrderedDict([('sender',tx['sender']), ('recipient' ,tx['recipient']), ('amount',tx['amount'])])
                updated_open_transactions.append(updated_tx)
            open_transactions = updated_open_transactions
    except IOError :
        print('-----------FILE NOT F O U N D-------------Initializing---')
        genesis_block = {
            'previous_hash' :'',
            'index' : 0,
            'transactions' : [],
            'proof' : 100
        }
        blockchain = [genesis_block]
        open_transactions = []
    
    finally:
        print('Clean up')
            
load_data()

def save_data():
    try :
        with open('blockchain.txt',mode = 'w') as f:
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
            #for pickle -------------------
            # save_data = {
            #     'chain' : blockchain,
            #     'ot' : open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError :
        print('saving Failed !')

def valid_proof(transactions, last_hash , proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    #print(guess)
    guess_hash = hash_string_256(guess)
    #print(guess_hash)
    return guess_hash[0:2] == '00' # My condition for valid hash


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions,last_hash, proof):
        proof += 1
    return proof

def get_balance(participant) :
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant] 
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0,tx_sender,0)
    
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = reduce(lambda tx_sum,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum +0,tx_recipient,0)
   
    return amount_recieved - amount_sent 

def get_last_blockchain_value():
    """ return the last value of the current blockchain"""
    if len(blockchain) < 1 :
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    else :
        return False


def add_transaction(recipient, sender = owner , amount = 1.0) :
    
    """ append the new value as well as the last value  to the new blockchain
    Arguments :
        : sender
        : reciepient
        : amount
    """
    # transaction = {
    #     'sender' : sender , 
    #     'recipient' : recipient , 
    #     'amount' : amount
    # }
    transaction = OrderedDict([('sender',sender), ('recipient' ,recipient), ('amount',amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender' : '-MINING-',
    #     'recipient' : owner,
    #     'amount' : MINING_REWARD
    # }
    reward_transaction = OrderedDict([('sender','MINING'),('recipient',owner), ('amount',MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash' :hashed_block,
        'index' : len(blockchain),
        'transactions' : copied_transactions,
        'proof' : proof
    }
    blockchain.append(block)
    #************************************
    return True


def get_transaction_value() :
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('your transaction amount please : '))
    return (tx_recipient, tx_amount)
     
    
def get_user_choice():
    user_input = input('your choice : ')
    return user_input

def print_bockchain_elements():
    for (i,block) in enumerate(blockchain) :
        print('Block Number : ' + str(i))
        print(block)
    else :  
        print('-'*20)


def verify_chain():
    for (index,block) in enumerate(blockchain):
        if index == 0 :
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'],block['proof']):
            print('Proof of Work is Invalid')
            return False
    return True

def verify_transactions():
   return all([verify_transaction(tx) for tx in open_transactions])

waiting_for_input = True

while waiting_for_input :
    print('please choose :')
    print('1 : Add a new transaction value : ')
    print('2 : Mine Block')
    print('3 : output the blockchain block :')
    print('4 : output Participants :')
    print('5 : Check transaction validity')
    print('h : manipulate the blockchain')
    print('q : Quit')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data =  get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient,amount= amount):
            print('Added Transaction')
        else :
            print('Transaction Failed')
        #print(open_transactions)

    elif user_choice == '2':
        if mine_block() :
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_bockchain_elements()

    elif user_choice == '4':
        print(participants)
    
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valide')
        else :
            print('There is invalid transaction')

    elif user_choice == 'h':
        if len(blockchain) >= 1 :
            blockchain[0]  = {
                            'previous_hash' :'',
                            'index' : 0,
                            'transactions' : [{'sender':'tom', 'recipient':'jack', 'amount':1000}]
                            }

    elif user_choice == 'q':
        waiting_for_input = False
    else :
        print('------input was invalid plsease choose from the list --------')
    if not verify_chain() :
        print_bockchain_elements()
        print("INVALID BLOCKCHAIN")
        break
    #print(get_balance('Rashadur'))
    print('Balance of {} : {:6.2f}'.format('Rashadur',get_balance('Rashadur')))
else :
    print('User left ')
    
print('DONE')
