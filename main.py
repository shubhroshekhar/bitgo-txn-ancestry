import requests

# UTILS
class TransactionAncestrySets:
    def __init__(self, height, max_txn_count=10):
        self.height = height
        self.max_txn_count = max_txn_count
        self.block_hash = self.get_hash_from_block_heoght()
        self.transactions = self.get_txns_from_hash()
    
    def get_hash_from_block_heoght(self):
        rqst = requests.get(f'https://blockstream.info/api/block-height/{self.height}')
        print(rqst.text)
        return rqst.text

    def get_txns_from_hash(self):
        rqst = requests.get(f'https://blockstream.info/api/block/{self.block_hash}/txs')
        print(rqst.text)
        return rqst.json()

    def get_linked_transactions_from_transaction(self, txn_id):
        rqst = requests.get(f'https://blockstream.info/api/tx/{txn_id}')
        print(rqst.text)
        import pdb; pdb.set_trace()
        return rqst.json()

# MAIN FLOW
def main():
    transaction_ancestry_sets = TransactionAncestrySets('680000', 10)
    print(transaction_ancestry_sets.transactions)





main()
