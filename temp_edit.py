import json

with open('ml_model.ipynb', 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_str = ''.join(cell['source'])
        if 'sample_conversation' in source_str:
            old = '''[

        {"speaker": "Agent", "text": "Hello, is this Mark Johnson? This is Sarah calling from XYZ Collections. How are you today?", "stime": 0, "etime": 8},

        {"speaker": "Customer", "text": "Hi Sarah, yes this is Mark. I'm doing okay, thanks.", "stime": 8.5, "etime": 12},

        {"speaker": "Agent", "text": "Thank you for that. Now, your current balance is $500. Would you like to discuss payment options?", "stime": 24, "etime": 34}

    ]'''
            new = '''[{"speaker": "Agent", "text": "Hello, is this Mark Johnson? This is Sarah calling from XYZ Collections. How are you today?", "stime": 0, "etime": 8}, {"speaker": "Customer", "text": "Hi Sarah, yes this is Mark. I'm doing okay, thanks.", "stime": 8.5, "etime": 12}, {"speaker": "Agent", "text": "Thank you for that. Now, your current balance is $500. Would you like to discuss payment options?", "stime": 24, "etime": 34}]'''
            source_str = source_str.replace(old, new)
            cell['source'] = [line + '\n' for line in source_str.split('\n') if line]

with open('ml_model.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
