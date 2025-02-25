# 🖥️ Laptop Data Scraper

## 📌 Description.
This script **parses information about laptops** from the [Nay.sk] website (https://www.nay.sk) and saves the data in **JSON** format.  
It gets the **name, specifications, price, and link** to the page of each laptop.

## 🚀 Functionality
✔ **Asynchronous parsing** using `aiohttp`.  
✔ **Blocks bypass** due to random **User-Agent** and delays between requests  
✔ **Saving data** in JSON format  
✔ **Error handling and retry** in case of server failures  

## 🛠️ Technologies used.
- **Python 3**.
- `aiohttp`, `BeautifulSoup`, `asyncio` - for asynchronous parsing
- `fake_useragent` - to avoid blocking
- `json`, `re` - for data processing  

## 📂 Output data format (laptops.json)
```json''
[
  {
    “about": {
      “type": “Gaming Laptop”,
      “Screen Size": “15.6 inches”,
      “Processor": “Intel Core i7”,
      “RAM": “16GB”,
      “Storage": “512GB SSD”,
      “GPU": “NVIDIA RTX 4060”,
      “Display Type": “IPS”,
      “Refresh Rate": “144Hz”,
      “Resolution": “1920x1080”,
      “Weight": “2.3kg”,
      “OS": “Windows 11”
    },
    “references": “https://www.nay.sk/laptop-example”,
    “price": “1299€”
  }
]

Translated with DeepL.com (free version)
