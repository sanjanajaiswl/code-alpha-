import csv
import statistics

def load_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean price string (e.g., "£42.96" -> 42.96)
            price_str = row['Price'].replace('£', '').replace('Â', '').strip()
            try:
                row['Price_Float'] = float(price_str)
            except ValueError:
                row['Price_Float'] = 0.0
            data.append(row)
    return data

def analyze_data(data):
    if not data:
        return {}
    
    prices = [row['Price_Float'] for row in data]
    avg_price = statistics.mean(prices)
    max_price = max(prices)
    min_price = min(prices)
    
    # Find books with max/min price
    most_expensive = [row['Title'] for row in data if row['Price_Float'] == max_price][0]
    least_expensive = [row['Title'] for row in data if row['Price_Float'] == min_price][0]
    
    # Rating distribution
    ratings = [row['Rating'] for row in data]
    rating_counts = {r: ratings.count(r) for r in set(ratings)}
    most_common_rating = max(rating_counts, key=rating_counts.get)
    
    # New insight: Price distribution
    under_20 = len([p for p in prices if p < 20])
    between_20_40 = len([p for p in prices if 20 <= p <= 40])
    over_40 = len([p for p in prices if p > 40])
    
    # New insight: Avg price by rating
    rating_prices = {}
    for row in data:
        r = row['Rating']
        p = row['Price_Float']
        if r not in rating_prices:
            rating_prices[r] = []
        rating_prices[r].append(p)
    avg_price_by_rating = {r: round(statistics.mean(p_list), 2) for r, p_list in rating_prices.items()}
    most_expensive_rating = max(avg_price_by_rating, key=avg_price_by_rating.get)
    
    return {
        'total_books': len(data),
        'avg_price': round(avg_price, 2),
        'max_price': max_price,
        'min_price': min_price,
        'most_expensive': most_expensive,
        'least_expensive': least_expensive,
        'rating_counts': rating_counts,
        'most_common_rating': most_common_rating,
        'under_20': under_20,
        'between_20_40': between_20_40,
        'over_40': over_40,
        'most_expensive_rating': most_expensive_rating,
        'most_expensive_rating_avg': avg_price_by_rating[most_expensive_rating]
    }

def generate_html(data, insights, output_filename):
    # CSS for a modern, beautiful, dynamic design
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Science Books Analysis</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --border: rgba(255, 255, 255, 0.1);
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
            animation: fadeInDown 1s ease-out;
        }}
        
        h1 {{
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: var(--text-muted);
            font-size: 1.2rem;
        }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
            margin-bottom: 50px;
        }}
        
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            animation: fadeInUp 0.8s ease-out forwards;
            opacity: 0;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            border-color: rgba(56, 189, 248, 0.3);
        }}
        
        .card:nth-child(1) {{ animation-delay: 0.1s; }}
        .card:nth-child(2) {{ animation-delay: 0.2s; }}
        .card:nth-child(3) {{ animation-delay: 0.3s; }}
        .card:nth-child(4) {{ animation-delay: 0.4s; }}
        
        .card h3 {{
            color: var(--text-muted);
            font-size: 1rem;
            font-weight: 600;
            margin-top: 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .card .value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
            margin: 10px 0;
        }}
        
        .card .detail {{
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.4;
        }}
        
        .data-section {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 30px;
            backdrop-filter: blur(10px);
            animation: fadeInUp 1s ease-out 0.6s forwards;
            opacity: 0;
            overflow-x: auto;
        }}
        
        .data-section h2 {{
            margin-top: 0;
            margin-bottom: 24px;
            font-size: 1.8rem;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        
        th, td {{
            padding: 16px;
            border-bottom: 1px solid var(--border);
        }}
        
        th {{
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }}
        
        tr {{
            transition: background-color 0.2s ease;
        }}
        
        tr:hover td {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        
        .rating-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.2);
        }}
        
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Science Books Insights</h1>
            <div class="subtitle">Data extracted from books.toscrape.com</div>
        </header>
        
        <div class="insights-grid">
            <div class="card">
                <h3>Total Books</h3>
                <div class="value">{insights['total_books']}</div>
                <div class="detail">Books analyzed in the Science category</div>
            </div>
            <div class="card">
                <h3>Average Price</h3>
                <div class="value">£{insights['avg_price']}</div>
                <div class="detail">Across all {insights['total_books']} books</div>
            </div>
            <div class="card">
                <h3>Price Extremes</h3>
                <div class="value">£{insights['max_price']}</div>
                <div class="detail">
                    <strong>Highest:</strong> {insights['most_expensive']}<br>
                    <strong>Lowest:</strong> £{insights['min_price']} ({insights['least_expensive']})
                </div>
            </div>
            <div class="card">
                <h3>Most Common Rating</h3>
                <div class="value">{insights['most_common_rating']} Stars</div>
                <div class="detail">
                    Out of {len(insights['rating_counts'])} different rating tiers observed
                </div>
            </div>
            <div class="card">
                <h3>Price Distribution</h3>
                <div class="value">{insights['between_20_40']}</div>
                <div class="detail">
                    Books between £20-£40<br>
                    ({insights['under_20']} under £20, {insights['over_40']} over £40)
                </div>
            </div>
            <div class="card">
                <h3>Priciest Tier</h3>
                <div class="value">{insights['most_expensive_rating']} Stars</div>
                <div class="detail">
                    Highest avg price: £{insights['most_expensive_rating_avg']}
                </div>
            </div>
        </div>
        
        <div class="data-section">
            <h2>Raw Dataset</h2>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Price</th>
                        <th>Rating</th>
                        <th>Availability</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for row in data:
        html_content += f"""
                    <tr>
                        <td>{row['Title']}</td>
                        <td>{row['Price']}</td>
                        <td><span class="rating-badge">{row['Rating']}</span></td>
                        <td>{row['Availability']}</td>
                    </tr>
"""

    html_content += """
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated HTML report at {output_filename}")

if __name__ == "__main__":
    csv_file = "science_books_dataset.csv"
    html_file = "index.html"
    
    print(f"Loading data from {csv_file}...")
    dataset = load_data(csv_file)
    
    print("Analyzing data...")
    dataset_insights = analyze_data(dataset)
    
    print("Generating HTML report...")
    generate_html(dataset, dataset_insights, html_file)
