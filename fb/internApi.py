import requests
import pandas as pd
from datetime import datetime, timedelta
import tqdm
import time
import random
import logging

logging.basicConfig(filename='request.log', level=logging.INFO)

def getData(st,et,offset,limit = 100):

    r = requests.get(f'https://api.qsearch.cc/api/trend/v1/posts?st={st}&et={et}&nation=TW&q=["實習"]&channels=["FB"]&limit={limit}&offset={offset}&key=c6efaa5ab04ddc241dd5cd7a80f0d6eaf5d21f69cdce596944292a12bdf0147b')
    return r



years = [2021]*12+[2022]*12
months = [i for i in range(1,13)]*2
days_e = [31,28,31,30,31,30,31,31,30,31,30,31]*2
st = datetime(2021,1,1)
ed = datetime(2021,1,31)
forums_m = []
medias_m =[]
for i in tqdm.tqdm(range(0,24)):
    st = datetime(year=years[i],month=months[i],day=1)
    et = datetime(year=years[i],month=months[i],day=days_e[i])
    off = 0
    
    forums = []
    
    while True:
        r = getData(st.strftime("%Y-%m-%d"),et.strftime("%Y-%m-%d"),offset=off)
        while r.status_code != 200:
            logging.info(f"retry: {st.strftime('%Y-%m-%d')} ~ {et.strftime('%Y-%m-%d')}, offset = {off}")
            print(f"retry: {st.strftime('%Y-%m-%d')} ~ {et.strftime('%Y-%m-%d')}, offset = {off}")
            time.sleep(random.random()*60)
            r = getData(st.strftime("%Y-%m-%d"),et.strftime("%Y-%m-%d"),offset=off)
            
        
        data = r.json()['data']

        forum = pd.concat([pd.DataFrame(data[k]['fb_raw']) for k in range(0,13)])
        # media = pd.concat([pd.DataFrame(data[k]['media_raw']) for k in range(0,13)])
        
        # forum.to_csv(f"./media_forum_data/forum_{st.strftime('%Y-%m-%d')}_{off}.csv")
        # media.to_csv(f"./media_forum_data/media_{st.strftime('%Y-%m-%d')}_{off}.csv")


        if (forum.shape[0] == 0):
            break
        
        forums.append(forum)

        logging.info(f"suc: {st.strftime('%Y-%m-%d')} ~ {et.strftime('%Y-%m-%d')}, offset = {off}")
        print(f"suc: {st.strftime('%Y-%m-%d')} ~ {et.strftime('%Y-%m-%d')}, offset = {off}")
        off+=300
        time.sleep(random.random()*10)
    
    pd.concat(forums).to_csv(f"./fb__data/forum_{st.strftime('%Y-%m-%d')}.csv")
    # pd.concat(medias).to_csv(f"./media_forum_data/media_{st.strftime('%Y-%m-%d')}.csv")

    forums_m.append(pd.concat(forums))
    # medias_m.append(pd.concat(medias))

    logging.info(f"get all suc: {st.strftime('%Y-%m-%d')} ~ {et.strftime('%Y-%m-%d')}")
    print(f"get all suc: {st.strftime('%Y-%m-%d')} ~ {et.strftime('%Y-%m-%d')}")
    time.sleep(random.random()*60)