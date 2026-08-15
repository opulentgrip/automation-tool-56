from typing import List, Dict, Any


def calculate_average_price(prices: List[float]) -> float:
    """
    Calculate the average price from a list of prices.

    Args:
        prices (List[float]): A list containing price values.

    Returns:
        float: The average price, or 0 if the list is empty.
    """
    return sum(prices) / len(prices) if prices else 0.0


def create_transaction_data(
    transaction_id: str, 
    amount: float, 
    currency: str, 
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create a structured transaction data dictionary.

    Args:
        transaction_id (str): The unique identifier for the transaction.
        amount (float): The amount of currency involved in the transaction.
        currency (str): The currency type of the transaction.
        metadata (Dict[str, Any], optional): Additional metadata related to the transaction.

    Returns:
        Dict[str, Any]: A dictionary containing structured transaction data.
    """
    return {
        'transaction_id': transaction_id,
        'amount': amount,
        'currency': currency,
        'metadata': metadata or {},
    }


def filter_transactions_by_currency(transactions: List[Dict[str, Any]], currency: str) -> List[Dict[str, Any]]:
    """
    Filter a list of transactions to include only those matching the specified currency.

    Args:
        transactions (List[Dict[str, Any]]): A list of transaction dictionaries.
        currency (str): The currency type to filter by.

    Returns:
        List[Dict[str, Any]]: A filtered list of transactions.
    """
    return [tx for tx in transactions if tx['currency'] == currency]