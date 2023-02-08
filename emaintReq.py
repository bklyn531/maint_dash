import requests
import json


class EmaintReq:
    def __init__(self, username, password, url) -> None:
        self.username = str(username)
        self.password = str(password)
        self.url = str(url)
        self.timeout = 10
        self.session = requests.Session()
        self.form_params = ['txtusername', 'txtpassword']
        self.payload = f'{self.form_params[0]}={self.username}&{self.form_params[1]}={self.password}&returnUrl=&BtnSubmit=Login&Login=Log+In'

    def login(self) -> None:
        post = self.session.get(url=self.url, data=self.payload)
        if post.status_code == 200:
            print('Login successful')
        elif post.status_code == 401:
            print('Invalid login authentication')
        elif post.status_code == 403:
            print('Invalid login credentials')

    async def get_tables(self, pages) -> list:
        table_url = 'https://x45.emaint.com/wc.dll?x3~emproc~x3hubv2~filelist~&TABLE=WORK&_=1675820196553'
        data_table = []
        print('Now reading data, please wait...')
        for page in pages:
            get_page = self.session.get(url=f'{table_url}', data=page)
            # time.sleep(5)
            page_text = get_page.text
            load_data = json.loads(page_text)
            data_table.append(load_data['data']['data'])
        print(f'Scrapped {len(data_table)} pages.')
        return data_table

    def write_data(self, data):
        file = open('data.json', 'w', encoding='utf8')
        print('writing data to file:', file.name, file.encoding)
        file.write(json.dumps(data))

    def filter_update(self) -> list:
        pages = []
        for page in range(1, 101):
            filters = f'~emproc~x3hubv2~filelist~&TABLE=WORK&FILTERS=%7B%7D&EXPLORERFILTER=%7B%7D&PFILTER=&SORT=%5B%7B"FIELD"%3A"WORK__DATE_WO"%2C"DIR"%3A"DESC"%7D%5D&PAGE={page}&PAGESIZE=100&JOIN=%7B%7D&GROUP=%5B%5D&EXTRAARGS=&ADVFILTUSED=&DYNFILTER=%7B%7D&COLUMNS=%5B%7B"FIELD"%3A"_MENU"%2C"WIDTH"%3A"22PX"%7D%2C%7B"FIELD"%3A"CHECK_ROW"%2C"WIDTH"%3A"30PX"%7D%2C%7B"FIELD"%3A"STAR_STATUS"%2C"WIDTH"%3A"26PX"%7D%2C%7B"FIELD"%3A"WORK__PROCESS001"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__WO"%2C"WIDTH"%3A118%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__DATE_WO"%2C"WIDTH"%3A124%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__COMPID"%2C"WIDTH"%3A136%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__COMP_DESC"%2C"WIDTH"%3A167%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__BRIEF_DESC"%2C"WIDTH"%3A235%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__WO_TYPE"%2C"WIDTH"%3A112%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__WORKSTATUS"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__STATTYPE"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__HOURS"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__RESPTIME"%2C"WIDTH"%3A76%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__ASSIGNTO"%2C"WIDTH"%3A89%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__COMMENTS"%2C"WIDTH"%3A687%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__DT_ASSIGN"%2C"WIDTH"%3A186%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__DT_CMPL"%2C"WIDTH"%3A160%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__REQ_CLA001"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%5D&_=1675813329965'
            pages.append(filters)
        return pages
