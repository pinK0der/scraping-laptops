import requests
from bs4 import BeautifulSoup
import json
import os
import re
import asyncio
import aiohttp
import time
import fake_useragent
import random

json_file = 'data/laptops.json'
start_time = time.time()
laptops = []

fake_usr = fake_useragent.UserAgent().random
header = {'User-Agent': fake_usr}

async def get_page_data(session, page, retry=5):
    link = f'https://www.nay.sk/nvidia-rtx?page={page}'
    link_temple = f'https://www.nay.sk'

    async with session.get(url=link, headers=header) as response:
        if response.status == 429:
            wait_time = random.randint(10, 30)  # random pause
            print(f"[WARNING] Rate limited! Waiting {wait_time} seconds before retrying...")
            await asyncio.sleep(wait_time)
            return await get_page_data(session, page, retry-1)

        if response.status != 200:
            print(f"[ERROR] Failed to fetch page {page}, status: {response.status}")
            return

        responce_text = await response.text()
        soupchink = BeautifulSoup(responce_text, "lxml")
        cards_list = soupchink.find_all('section', class_='product-box position-relative typo-complex-12 product-box--main bs-p-3 bs-p-lg-4 bg-white flex-grow-0 flex-shrink-0')

        for card in cards_list:
            try:
                link_for_laptop = card.find('a', class_='product-box__link').get('href')

                req_laptop = await session.get(f'{link_temple}{link_for_laptop}', headers=header)

                if req_laptop.status == 429:
                    wait_time = random.randint(10, 30)
                    print(f"[WARNING] Rate limited! Waiting {wait_time} seconds before retrying...")
                    await asyncio.sleep(wait_time)
                    continue

                print(f'[+] {link_temple}{link_for_laptop} {req_laptop.status}')

                req_laptop_text = await req_laptop.text()
                soup_laptop = BeautifulSoup(req_laptop_text, "lxml")

                info_laptop = soup_laptop.find('p', class_='product-box__parameters product-top__section order-3 typo-complex-14 typo-complex-lg-16').text

                # price
                price = soup_laptop.find('strong', class_='block text-22 whitespace-nowrap lg:text-32').text.strip(' ')

                # try to sort info about laptop
                specs = re.split(r',\s*(?=\D)', info_laptop)

                if len(specs) == 10:
                    laptop_data = {
                        "Type": specs[0],
                        "Screen Size": specs[1],
                        "Processor": specs[2],
                        "RAM": specs[3].replace("RAM ", ""),
                        "Storage": specs[4].replace("SSD ", ""),
                        "GPU": specs[5].replace("GPU: ", ""),
                        "Display Type": 'IPS',
                        "Refresh Rate": specs[6],
                        "Resolution": specs[7],
                        "Weight": specs[8],
                        "OS": specs[9],
                    }
                elif len(specs) == 11:
                    laptop_data = {
                        "Type": specs[0],
                        "Screen Size": specs[1],
                        "Processor": specs[2],
                        "RAM": specs[3].replace("RAM ", ""),
                        "Storage": specs[4].replace("SSD ", ""),
                        "GPU": specs[5].replace("GPU: ", ""),
                        "Display Type": specs[6],
                        "Refresh Rate": specs[7],
                        "Resolution": specs[8],
                        "Weight": specs[9],
                        "OS": specs[10],
                    }

                data_about = {
                    "about": laptop_data,
                    "link": f'{link_temple}{link_for_laptop}',
                    "price": price,
                }

                laptops.append(data_about)
                print(f'save info about laptop from page {page} to list')

            except Exception as e:
                if retry:
                    print(f'[INFO] retry={retry} => {link_temple}{link_for_laptop}')
                    await asyncio.sleep(5)
                    return await get_page_data(session, page, retry - 1)
                else:
                    print(f'[ERROR] Failed after multiple retries: {e}')

async def gather_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://www.nay.sk/nvidia-rtx?page=', headers=header)
        if response.status == 429:
            wait_time = random.randint(10, 30)
            print(f"[WARNING] Rate limited! Waiting {wait_time} seconds before retrying...")
            await asyncio.sleep(wait_time)
            return await gather_data()

        soup = BeautifulSoup(await response.text(), 'lxml')
        page_count = int(soup.find('ul', class_='pagination b-pagination justify-content-center').find_all('li')[-2].text)

        tasks = []

        for page in range(1, page_count + 1):
            try:
                task = asyncio.create_task(get_page_data(session, page))
                print(f'added task {page} to list')
                tasks.append(task)
                await asyncio.sleep(random.uniform(1, 5))
            except Exception as e:
                print(f'failed to add task {page} to list: {e}')
                continue

        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(laptops, file, indent=4, ensure_ascii=False)
    finish_time = time.time() - start_time
    print(f'Time for script work: {finish_time}')

    # 83.5 sec, while old one work 325s

if __name__ == '__main__':
    main()
