
import streamlit as st

# EDA Pkgs
import pandas as pd
import numpy as np
import os

# Plotting Pkgs
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image,ImageFilter,ImageEnhance
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import base64

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

st.set_page_config(layout='wide')
st.title("RISS 논문 크롤링과 데이터 분석")
st.subheader("Web App for Python Crawling and EDA with Streamlit ")
st.markdown("""
    #### --- 누구나 쉽게 자신만의 데이터분석 웹 어플리케이션을 만들 수 있다.!:sunglasses:
    
    """)
expander_bar = st.beta_expander("Quick Guide")
expander_bar.markdown("""
1. 왼쪽 사이드바 메뉴에서 크롤링과 데이터 분석 중 하나를 선택합니다.  
2. 
3.
4.
""")

st.sidebar.header('메뉴를 선택하세요')
menu = ["논문 정보 수집","논문 키워드 수집", "Word Cloud", "Topic Modeling"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "논문 정보 수집":
    

    keyword = st.text_input("검색할 논문의 키워드를 입력하세요(예:로봇, 인공지능+교육): ")
    if st.checkbox("결과 확인!"):
        url = f"http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery={keyword}&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=0\
        &orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&fsearchMethod=&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale=100\
        &isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query={keyword}"
        result = requests.get(url, headers=headers)
        if result.status_code == 200:

            soup = bs(result.content, 'html.parser')
            max_num = soup.find('span', class_='num').text
            st.text(f"총{max_num}개의 논문이 검색되었습니다. ")
        else :
            st.text("woops! 다음에 다시 시도해주세요.")

    number= st.text_input("이 중 몇 개를 가져올까요?(최대 1,000개):")
    st.markdown("""숫자를 입력하고 엔터키를 누릅니다! 
    아래 **크롤링 시작!** 버튼을 클릭하면 크롤링이 시작되고 잠시 후 결과가 나타납니다.!""")
    url = f"http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery={keyword}&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=0&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&fsearchMethod=&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale={number}&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query={keyword}"

    if st.checkbox("크롤링 시작!"):

        result = requests.get(url, headers=headers)
        soup = bs(result.content, 'html.parser')
        contents = soup.find_all('div', class_='cont')

        title =[]
        writer = []
        society = []
        year = []
        journal = []
        link =[]
        abstracts=[]


        for cont in contents:

            title_temp = cont.find('p', class_='title').text
            #print(title_temp)
            title.append(title_temp)
            writer_temp = cont.find('span', class_ = 'writer').text
            writer.append(writer_temp)

            society.append(cont.find('span', class_ = 'assigned').text)

            year.append(cont.find('p', class_='etc').find_all('span')[2].text)  # <p class='etc'>에서 3번째 span tag에 있는 텍스트

            journal.append(cont.find('p', class_='etc').find_all('span')[3].text)

            link.append("http://www.riss.kr"+cont.find('p', class_='title').a['href']) # <p, class='title'>의 a 태그의 'href' 속성 값

            if cont.find('p', class_='preAbstract') :
                abstracts.append(cont.find('p', class_='preAbstract').text)
                
            else:
                abstracts.append("초록이 없습니다.")


        with st.spinner("Waiting .."):
            time.sleep(5)
        st.success("데이터 수집에 성공하였습니다.!!")

        df = pd.DataFrame(
            {"title":title,
             "writer":writer,
             "society":society,
             "year":year,
             "journal":journal,
             "link":link,
            "abstracts":abstracts}
        )

        st.dataframe(df)

    st.text("""excel 또는 csv파일로 수집한 내용을 저장할 수 있습니다.
    파일 이름은 '키워드+논문개수'로 자동 생성됩니다 예)'인공지능10.csv""")
    
    if st.checkbox("파일 저장"):

        select=st.selectbox('어떤 파일로 저장할까요?', ['excel파일','csv파일','둘 다'])

        if select == 'excel파일':
            df.to_excel(f'{keyword}{number}.xlsx', index=False)

        elif select == 'csv파일':
            df.to_csv(f'{keyword}{number}.csv', index=False)

        elif select == '둘 다':
            df.to_csv(f'{keyword}{number}.csv', index=False)
            df.to_excel(f'{keyword}{number}.xlsx', index=False)

        st.text("수고하셨습니다. 사이드 메뉴에서 키워드 크롤링도 시도해보세요!")

elif choice == "논문 키워드 수집":
    pass

elif choice == "word cloud":
    
    st.text("크롤링으로 저장한 csv파일을 불러와서 분석을 시작해봅시다!")
    data_file = st.file_uploader("Upload CSV",type=['csv'])

    if data_file is not None:
        df = pd.read_csv(data_file)
        st.dataframe(df)

    if st.checkbox("Preview DataFrame"):
        if st.button("처음 5개 데이터"):
            st.write(df.head())
        if st.button("마지막 5개 데이터"):
            st.write(df.tail())

    if st.checkbox("컬럼 이름과 데이터 수 확인"):
        st.text("Columns:")
        st.write(df.columns)
        st.text("No. of Data:")
        st.write(len(df))

    counts = st.selectbox('Select Columns',('writer','year','society'))
    st.set_option('deprecation.showPyplotGlobalUse', False)
    from matplotlib import font_manager, rc
    font_path = "./font/NanumGothic.ttf"

    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    st.write("저자, 발행연도, 발행기관별로 빈도수를 분석합니다.! ")


    if counts=="writer":
        st.write(df["writer"].value_counts())
        df['writer'].value_counts().head(10).plot(kind="pie", label='', autopct='%.1f%%', shadow=True, cmap="YlGnBu", counterclock=False, startangle=90)
        st.pyplot()

    if counts=="year":
        st.write(df["year"].value_counts())
        df['year'].value_counts().head(10).plot(kind="pie", label='', autopct='%.1f%%', shadow=True, cmap="rainbow", counterclock=False, startangle=90)
        st.pyplot()

    if counts=="society":
        st.write(df["society"].value_counts())
        df['society'].value_counts().head(10).plot(kind="pie", label='', autopct='%.1f%%', shadow=True, cmap="Blues", counterclock=False, startangle=90)
        st.pyplot()

    if st.checkbox("빈도수 분석"):

        st.text("단어 빈도수 분석 : 상위 50개 명사 출력")

        import konlpy
        from konlpy.tag import Okt  
        okt=Okt() 

        title = df["title"]

        nouns=[]
        stop_words=''
        for words in title: 
            for noun in okt.nouns(words):
                if noun not in stop_words and len(noun)>1: 
                    nouns.append(noun) 


        from collections import Counter

        num_top_nouns = 50
        nouns_counter = Counter(nouns)
        top_nouns = dict(nouns_counter.most_common(num_top_nouns))
        st.text (top_nouns)

        st.text("텍스트분석에서 제거할 단어, 즉 불필요한 단어를 띄어쓰기 기준으로 적어주세요.")

        nouns=[]
        stop_words= st.text_input("불용어: ")


        for words in title: 
            for noun in okt.nouns(words):
                if noun not in stop_words and len(noun)>1: 
                    nouns.append(noun) 

        num_top_nouns = 50
        nouns_counter = Counter(nouns)
        top_nouns = dict(nouns_counter.most_common(num_top_nouns))


    if st.checkbox("WordCloud 생성"):
    #         bg_color = st.selectbox("배경색",['white','yellow','green','grey'])
        random_number = st.slider("슬라이를 움직여 바뀌는 그림을 확인해보세요.",0,100)

        from wordcloud import WordCloud

        wordcloud = WordCloud (
        max_words= 200,  
        background_color = "white",  
        random_state = random_number,

        font_path = "./font/NanumGothic.ttf")

        wc = wordcloud.generate_from_frequencies(top_nouns)
        plt.figure(figsize=(8,8))
        plt.imshow(wc)     
        plt.axis('off')    ## 가로, 세로축을 별도로 표시하지 않음.
        # plt.savefig('bts.png')    ## 그림을 저장함.
        st.pyplot()

elif choice == "Topic Modeling":
    if st.checkbox("토픽모델링"):  

        import gensim.corpora as corpora
        from gensim.models.ldamodel import LdaModel 

        from gensim.models import CoherenceModel

        stop_words=stop_words.split(' ')

        tokenized_doc = df['title'].str.replace('[^ㄱ-ㅎㅏ-ㅣ가-힣|0-9]',' ',regex=True)
        tokenized_doc = df["title"].apply(lambda x: okt.nouns(x)) # 명사 토큰화

        tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stop_words and len(item)>1])

        dictionary = corpora.Dictionary(tokenized_doc)
        corpus = [dictionary.doc2bow(text) for text in tokenized_doc]

        model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
        st.write(model.print_topics())

    if st.checkbox("토픽모델링 시각화"):  

        import pyLDAvis
        import pyLDAvis.gensim as gensimvis
        prepared_data = gensimvis.prepare(model, corpus, dictionary)
    #         pyLDAvis.display(prepared_data)

        html_string = pyLDAvis.prepared_data_to_html(prepared_data)
        from streamlit import components
        components.v1.html(html_string, width=1200, height=600, scrolling=True)
