


from app.models.transactions import Transaction


def fraud_check(transaction: Transaction) -> bool:
    
    if transaction.amount > 10000:  # Example threshold for fraud
        return True
    if transaction.sender_id == transaction.receiver_id:
        return True
    
    return False