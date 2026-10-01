import platform
import sys
import aiohttp
import asyncio
from datetime import datetime, timedelta

date =datetime.now().strftime("%d.%m.%Y") 
API =(f"https://api.privatbank.ua/p24api/exchange_rates?date={date}")

async def processing(html):
    
                currency=[]
                for i in html["exchangeRate"]:              #Знаходимо курси саме EUR i USD
                    if i.get("currency") in ("EUR", "USD"):
                        currency.append(i)
                return currency

async def main(API):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API) as response:
                html = await response.json()
            return await processing(html)

        except aiohttp.ClientConnectorError as err:         #Якщо сайт не відповідає
            print("Connection error:", str(err))

async def cycle(count_of_days):
    tasks={}
    for i in range (0,count_of_days):        #Цикл якй додає у словник як ключ -дату і як значення - корутину 
        date =datetime.now()
        api =(f"https://api.privatbank.ua/p24api/exchange_rates?date={(date-timedelta(days=i)).strftime("%d.%m.%Y")}")
        tasks[(f"{(date-timedelta(days=i)).strftime("%d.%m.%Y")}")]=main(api)

    functions=await asyncio.gather(*tasks.values()) #Чекаєио поки корутини виконаються і створюємо список з результатів у правильному порядку
    dates=tasks.keys()
    result=dict(zip(dates,functions))     #Словник з датою та знайденим курсом 
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:       #Якщо користувач нічого не ввів - за замовчування перевіряємо курс за поточний день 
        try:
            count_of_days = int(sys.argv[1])
        except ValueError:
            print("Можна вводити лише число")
        else:
            if count_of_days not in range(1, 11):
                print("Дату можна взнати в діапазоні від 1 до 10 останніх днів")
            else:
                res=asyncio.run(cycle(count_of_days))
                print(res)

    else:
        count_of_days = 1
        res=asyncio.run(cycle(count_of_days))
        print(res)


