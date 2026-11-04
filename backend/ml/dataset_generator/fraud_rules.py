def calculate_risk(transaction):

    score = 0

    if transaction["amount"] > 3000:
        score += 30

    if transaction["device_type"] == "Mobile":
        score += 10

    if transaction["payment_method"] == "Credit Card":
        score += 10

    if transaction["transaction_hour"] <= 5:
        score += 20

    if transaction["country"] != "United States":
        score += 20

    return score