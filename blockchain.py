import functools
MINING_REWARD = 10
genesis_block = {
        'previous_hash' :'',
        'index' : 0,
        'transactions' : []
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Rashadur'
participants = {'Rashadur'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def get_balance(participant) :
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant] 
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(lambda tx_sum,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0,tx_sender,0)
    
    
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum,tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum +0,tx_recipient,0)
   
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
    
    transaction = {
        'sender' : sender , 
        'recipient' : recipient , 
        'amount' : amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    #print(hashed_block)
    reward_transaction = {
        'sender' : '-MINING-',
        'recipient' : owner,
        'amount' : MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash' :hashed_block,
        'index' : len(blockchain),
        'transactions' : copied_transactions
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
        print(open_transactions)

    elif user_choice == '2':
        if mine_block() :
            open_transactions = []

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
