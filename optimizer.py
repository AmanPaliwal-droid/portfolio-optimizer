import csv
import argparse
import matplotlib.pyplot as plt

def read_assets(csv_file):
    assets = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assets.append({
                'Ticker': row['Ticker'],
                'ExpectedReturn': float(row['ExpectedReturn(%)']),
                'RiskScore': int(row['RiskScore(0-100)']),
                'Price': int(row['Price'])
            })
    return assets

def knapsack_dp(assets, capital):
    n = len(assets)
    C = capital
    # DP table: (n+1) x (C+1)
    dp = [[0]*(C+1) for _ in range(n+1)]
    keep = [[False]*(C+1) for _ in range(n+1)]

    for i in range(1, n+1):
        price = assets[i-1]['Price']
        ret = assets[i-1]['ExpectedReturn']
        for w in range(C+1):
            if price <= w:
                if dp[i-1][w-price] + ret > dp[i-1][w]:
                    dp[i][w] = dp[i-1][w-price] + ret
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]

    # Backtrack to find selected assets
    w = C
    selected = []
    for i in range(n, 0, -1):
        if keep[i][w]:
            selected.append(assets[i-1])
            w -= assets[i-1]['Price']
    selected.reverse()
    return selected

def filter_by_risk(selected, risk_tolerance):
    # If total risk > tolerance, drop lowest return asset and retry
    while True:
        total_risk = sum(a['RiskScore'] for a in selected)
        if total_risk <= risk_tolerance or len(selected) == 0:
            break
        # Remove asset with worst return
        worst = min(selected, key=lambda x: x['ExpectedReturn'])
        selected.remove(worst)
    return selected

def total_cost(assets):
    return sum(a['Price'] for a in assets)

def total_return(assets):
    return sum(a['ExpectedReturn'] for a in assets)

def total_risk(assets):
    return sum(a['RiskScore'] for a in assets)

def run_optimizer(assets, capital, risk_tolerance):
    selected = knapsack_dp(assets, capital)
    filtered = filter_by_risk(selected, risk_tolerance)
    return filtered

def sweep_risk_frontier(assets, capital):
    frontier = []
    for risk_tol in range(0, 101, 5):
        selected = run_optimizer(assets, capital, risk_tol)
        r = total_return(selected)
        risk = total_risk(selected)
        frontier.append((risk, r))
    return frontier

def plot_frontier(frontier):
    x = [point[0] for point in frontier]
    y = [point[1] for point in frontier]
    plt.figure(figsize=(8,5))
    plt.scatter(x, y, c='blue')
    plt.title('Efficient Frontier: Risk vs Expected Return')
    plt.xlabel('Risk Score')
    plt.ylabel('Expected Return (%)')
    plt.grid(True)
    plt.savefig('frontier.png')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Portfolio Optimizer')
    parser.add_argument('--capital', type=int, required=True, help='Capital available')
    parser.add_argument('--risk', type=int, required=True, help='Risk tolerance (0-100)')
    parser.add_argument('--csv', type=str, required=True, help='CSV file with assets')
    parser.add_argument('--plot', action='store_true', help='Plot efficient frontier')
    args = parser.parse_args()

    assets = read_assets(args.csv)
    selected = run_optimizer(assets, args.capital, args.risk)

    if len(selected) == 0:
        print("No assets selected within given constraints.")
        return

    print(f"Selected {len(selected)} assets:")
    print(' '.join([a['Ticker'] for a in selected]))
    print(f"Total Cost : ₹{total_cost(selected):,}")
    print(f"Exp Return : {total_return(selected):.1f} %")
    print(f"Risk Score : {total_risk(selected)}")

    if args.plot:
        frontier = sweep_risk_frontier(assets, args.capital)
        plot_frontier(frontier)
        print("Frontier plot saved to frontier.png")

if __name__ == "__main__":
    main()
