import json
from pathlib import Path
import hw3

with open('public_test/ground_truth.json') as f:
    truth = json.load(f)

print(f"{'Company':25} | P12 | C26/Rev | C28>C26? | R&D_Growth")
for c in truth:
    p12 = truth[c]['points']['12']
    sql = hw3.make_tools(Path(f'public_test/{c}'))[2]
    
    q = """
    WITH cap AS (
        SELECT 
            MAX(CASE WHEN year=2026 THEN planned_capex END) as c26,
            MAX(CASE WHEN year=2028 THEN planned_capex END) as c28
        FROM capex_plan
    ),
    rev AS (
        SELECT SUM(amount) as r25 FROM orders WHERE order_date LIKE '2025%'
    ),
    rd AS (
        SELECT 
            SUM(CASE WHEN month LIKE '2024%' THEN research_development END) as rd24,
            SUM(CASE WHEN month LIKE '2025%' THEN research_development END) as rd25
        FROM monthly_costs
    )
    SELECT c26, c28, r25, rd24, rd25 FROM cap, rev, rd
    """
    res = sql.invoke({"query": q})
    lines = res.split('\n')
    if len(lines) > 1:
        vals = lines[1].split('|')
        def f(v): 
            v = v.strip()
            return float(v) if v and v != 'None' else 0.0
        c26, c28, r25, rd24, rd25 = f(vals[0]), f(vals[1]), f(vals[2]), f(vals[3]), f(vals[4])
        
        cap_rev = c26 / r25 * 100 if r25 else 0
        c_increase = "YES" if c28 > c26 else "NO"
        rd_growth = (rd25 - rd24) / rd24 * 100 if rd24 else 0
        
        print(f"{c[:25]:25} | {p12} | {cap_rev:7.1f}% | {c_increase:8} | {rd_growth:9.1f}%")
