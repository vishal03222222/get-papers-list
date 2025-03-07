import csv
from typing import List, Dict

def save_to_csv(data: List[Dict], filename: str) -> None:
    if not data:
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)