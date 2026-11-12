import json
import csv

with open('public_test/ground_truth.json', 'r') as f:
    truth_data = json.load(f)

results = {}
with open('results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        points_dict = {}
        if row['points']:
            for item in row['points'].split():
                if ':' in item:
                    p, v = item.split(':')
                    points_dict[p] = v
        results[row['company']] = points_dict

print("=== 錯誤分析 ===")
error_count = 0
for company, info in truth_data.items():
    expected_points = info['points']
    actual_points = results.get(company, {})
    
    for point in ['5', '12', '13']:
        exp = expected_points.get(point)
        act = actual_points.get(point)
        
        if exp != act:
            print(f"[{company}] Point {point}: 預期 {exp}, 你給 {act}")
            error_count += 1

print(f"\n總共發現 {error_count} 個錯誤 (總題數 60)。")
