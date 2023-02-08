import time
import asyncio
from emaintReq import EmaintReq


async def main():
    start = int(time.perf_counter())
    instance = EmaintReq(username='idemia1', password='adminidemia',
                         url='https://x45.emaint.com/wc.dll?X3~dologin~&loc=en&languageid=en')
    instance.login()
    get_pages = instance.filter_update()
    get_data = await instance.get_tables(get_pages)
    instance.write_data(get_data)
    stop = int(time.perf_counter())
    print(f'Time elapsed: {stop - start}s')

if __name__ == '__main__':
    asyncio.run(main())
