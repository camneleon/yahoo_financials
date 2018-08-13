# Request finance data

Scrape yahoo finance financials and save as JSON file for later use. See *financial_statements.json* for example output.

## Intention

Fun little project, also shows the ease of getting data out of HTML and converting it to somwthing usable.

## Getting Started

*Note* Use sparingly... rate limit or do whatever to reduce requests. Don't go too crazy.

```
in command line run
python yahoo_finance_scrape.py
```

changing request
Change PAYLOADS *NOTE: **ONLY** change the ticker in this example APX.AX* 
```python
PAYLOADS = [['balance-sheet', 'APX.AX'],
            ['financials', 'APX.AX'],
            ['cash-flow', 'APX.AX']]
```
Example change would be as follows or you could load a csv as long as it's loaded as a list of list in same order. 
```python
PAYLOADS = [['balance-sheet', 'APX.AX'],
            ['financials', 'APX.AX'],
            ['cash-flow', 'APX.AX']
            ['balance-sheet', 'NCM.AX'],
            ['financials', 'NCM.AX'],
            ['cash-flow', 'NCM.AX']]
```
## Required

* **requests**
* **beautifulsoup4**
### OR 
```
pip install -r requirments.txt
```