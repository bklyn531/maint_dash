import asyncio
import json
import requests
import os

txtusername = 'idemia1'
txtpassword = 'adminidemia'
work_table = 'https://x45.emaint.com/wc.dll?x3~emproc~x3hubv2~filelist~&TABLE=WORK&q=GetListData&__=69uRXR'
login_url = "https://x45.emaint.com/wc.dll?X3~dologin~&loc=en&languageid=en"
login_payload = f'txtusername={txtusername}&txtpassword={txtpassword}&returnUrl={work_table}&BtnSubmit=Login&Login=Log+In'
data_table = []
filters = []
pages = []
headers = {"content-type": "application/json"}


def create_session():
    request_obj = requests.Session()
    return request_obj


session = create_session()


def login():
    s = session.post(login_url, data=login_payload)
    print(f'connection successful {s.status_code}')
    return s


async def filter_update():
    pages = []
    for page in range(1, 11):
        filter = f'&filters=%7B%7D&explorerFilter=%7B%7D&pfilter=&sort=%5B%7B%22field%22%3A%22work__date_wo%22%2C%22dir%22%3A%22desc%22%7D%5D&page={page}&pageSize=100&join=%7B%7D&group=%5B%5D&extraArgs=&advFiltUsed=&dynFilter=%7B%7D&columns=%5B%7B%22field%22%3A%22_menu%22%2C%22width%22%3A%2222px%22%7D%2C%7B%22field%22%3A%22check_row%22%2C%22width%22%3A%2230px%22%7D%2C%7B%22field%22%3A%22star_status%22%2C%22width%22%3A%2226px%22%7D%2C%7B%22field%22%3A%22work__process001%22%2C%22width%22%3A70%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__wo%22%2C%22width%22%3A118%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__date_wo%22%2C%22width%22%3A124%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__compid%22%2C%22width%22%3A136%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__comp_desc%22%2C%22width%22%3A167%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__brief_desc%22%2C%22width%22%3A235%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__wo_type%22%2C%22width%22%3A112%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__workstatus%22%2C%22width%22%3A70%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__stattype%22%2C%22width%22%3A70%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__hours%22%2C%22width%22%3A70%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__resptime%22%2C%22width%22%3A76%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__assignto%22%2C%22width%22%3A89%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__comments%22%2C%22width%22%3A687%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__dt_assign%22%2C%22width%22%3A186%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__dt_cmpl%22%2C%22width%22%3A160%2C%22aggtype%22%3A%22%22%7D%2C%7B%22field%22%3A%22work__req_cla001%22%2C%22width%22%3A70%2C%22aggtype%22%3A%22%22%7D%5D'
        pages.append(filter)
    return pages


async def get_data_tables():
    session = create_session()
    s = session.post(login_url, data=login_payload)
    print(f'connection successful {s.status_code}')

    for filter in pages:
        r = session.request('GET', work_table+filter, headers=headers)
        text = r.text
        load_data = json.loads(text)
        data_table.append(load_data['data'])
        print('appending to data table')
    return data_table


async def write_to_file():
    file = open('data.json', 'w')
    print('Writing to file: ')
    file.write(json.dumps(data_table))


async def main():
    print('Starting')
    create_session()
    login()
    await get_data_tables()
    print(data_table)
    print(pages)
    print('Table created')
    await write_to_file()


if __name__ == '__main__':
    asyncio.run(main())
