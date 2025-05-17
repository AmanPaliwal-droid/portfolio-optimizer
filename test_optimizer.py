import pytest
from optimizer import knapsack_dp

def test_knapsack_higher_return():
    # Mini fixture with 5 assets
    assets = [
        {'Ticker': 'A', 'ExpectedReturn': 10, 'RiskScore': 20, 'Price': 50},
        {'Ticker': 'B', 'ExpectedReturn': 20, 'RiskScore': 30, 'Price': 60},
        {'Ticker': 'C', 'ExpectedReturn': 15, 'RiskScore': 10, 'Price': 70},
        {'Ticker': 'D', 'ExpectedReturn': 40, 'RiskScore': 25, 'Price': 80},
        {'Ticker': 'E', 'ExpectedReturn': 30, 'RiskScore': 40, 'Price': 90},
    ]

    capital = 150
    selected = knapsack_dp(assets, capital)
    total_return = sum(a['ExpectedReturn'] for a in selected)
    total_price = sum(a['Price'] for a in selected)

    # For same capital, should prefer assets with higher return
    assert total_price <= capital
    assert total_return >= 50  # Expecting high return selected

if __name__ == "__main__":
    pytest.main()
