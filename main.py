import requests
from operator import itemgetter

class TransactionAncestrySets:
    """Transaction Ancestry base class
    Load class with block height 
    """
    def __init__(self, height):
        self.height = height
        self.block_hash = self.__get_hash_from_block_heoght()
        self.transactions = self.__get_txns_from_hash()
        self.__updated_transactions()
    
    def __get_hash_from_block_heoght(self):
        """get hash from given block height 

        Returns:
            str: block hash
        """
        rqst = requests.get(f'https://blockstream.info/api/block-height/{self.height}')
        return rqst.text

    def __get_txns_from_hash(self):
        """gets transaction from hash
        Returns:
            dict: transaction details 
        """
        rqst = requests.get(f'https://blockstream.info/api/block/{self.block_hash}/txs')
        return rqst.json()

    def get_transactions_detail_from_transaction_id(self, txn_id):
        """loads transaction details from transaction id

        Args:
            txn_id (str): transaction_id

        Returns:
            dict: transaction detals
        """
        rqst = requests.get(f'https://blockstream.info/api/tx/{txn_id}')
        print(f'getting txn details - {txn_id}')
        txn_detail = rqst.json()
        return txn_detail

    def __updated_transactions(self):
        """loads details of every transaction 
        """
        for x in self.transactions:
            if x['status']['block_hash'] == self.block_hash:
                trahsaction_details = self.get_transactions_detail_from_transaction_id(x['txid'])
                x['txn_detail_data'] = trahsaction_details
                # Assuming vin is the ancestry history list of the transaction 
                x['count'] = len(trahsaction_details['vin'])
            else:
                x['txn_detail_data'] = None
                x['count'] = 0
        self.transactions = sorted(self.transactions, key=itemgetter('count'), reverse=True)
    
    def get_top_txns(self, max_txn_count):
        """get top transactions

        Args:
            max_txn_count (int): count of transaction

        Returns:
            list: top transaction with max ancestry
        """
        n_l = []
        c = max_txn_count if len(self.transactions) >= max_txn_count else  len(self.transactions)
        for x in range(c):
            n_l.append({"txid" : self.transactions[x]["txid"], "ancestrySetSize": self.transactions[x]['count']})
        return n_l

# MAIN FLOW
def main():
    transaction_ancestry_sets = TransactionAncestrySets('680000')
    print(transaction_ancestry_sets.get_top_txns(100))

main()

