from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import time

dataTable = []


def emaintReq(page):
    start_t = int(time.perf_counter())
    url = 'https://x45.emaint.com/wc.dll?X3~dologin~&loc=en&languageid=en'
    payload = 'txtusername=idemia1&txtpassword=adminidemia&returnUrl=&BtnSubmit=Login&Login=Log+In'
    with requests.Session() as s:
        s.get(url=url, data=payload)

    tableUrl = 'https://x45.emaint.com/wc.dll?x3~emproc~x3hubv2~filelist~&TABLE=WORK&_=1675820196553'
    req = s.get(url=tableUrl, data=page).text
    loadData = json.loads(req)['data']['data']
    end_t = int(time.perf_counter())
    return loadData, end_t - start_t


def main():
    start = int(time.perf_counter())
    pages = []

    for page in range(1, 1021):
        data_filter = f'~emproc~x3hubv2~filelist~&TABLE=WORK&FILTERS=%7B%7D&EXPLORERFILTER=%7B%7D&PFILTER=&SORT=%5B%7B"FIELD"%3A"WORK__DATE_WO"%2C"DIR"%3A"DESC"%7D%5D&PAGE={page}&PAGESIZE=100&JOIN=%7B%7D&GROUP=%5B%5D&EXTRAARGS=&ADVFILTUSED=&DYNFILTER=%7B%7D&COLUMNS=%5B%7B"FIELD"%3A"_MENU"%2C"WIDTH"%3A"22PX"%7D%2C%7B"FIELD"%3A"CHECK_ROW"%2C"WIDTH"%3A"30PX"%7D%2C%7B"FIELD"%3A"STAR_STATUS"%2C"WIDTH"%3A"26PX"%7D%2C%7B"FIELD"%3A"WORK__PROCESS001"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__WO"%2C"WIDTH"%3A118%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__DATE_WO"%2C"WIDTH"%3A124%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__COMPID"%2C"WIDTH"%3A136%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__COMP_DESC"%2C"WIDTH"%3A167%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__BRIEF_DESC"%2C"WIDTH"%3A235%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__WO_TYPE"%2C"WIDTH"%3A112%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__WORKSTATUS"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__STATTYPE"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__HOURS"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__RESPTIME"%2C"WIDTH"%3A76%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__ASSIGNTO"%2C"WIDTH"%3A89%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__COMMENTS"%2C"WIDTH"%3A687%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__DT_ASSIGN"%2C"WIDTH"%3A186%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__DT_CMPL"%2C"WIDTH"%3A160%2C"AGGTYPE"%3A""%7D%2C%7B"FIELD"%3A"WORK__REQ_CLA001"%2C"WIDTH"%3A70%2C"AGGTYPE"%3A""%7D%5D&_=1675813329965'
        pages.append(data_filter)

    with Pool(processes=16) as pool:
        results = pool.map(emaintReq, pages)
        for data, duration in results:
            dataTable.append(data)
            print(f'Page completed in {duration}s')
    print(f'Total time to complete: {int(time.perf_counter()) - start}s')


if __name__ == '__main__':
    main()
    file = open('data.json', 'w', encoding='utf8')
    file.write(json.dumps(dataTable))
