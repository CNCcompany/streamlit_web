import streamlit as st
import requests
import pandas as pd

from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt

#페이지 기타 세팅
st.set_page_config(page_title="Crema App", page_icon="🤖")
session = requests.Session()

#불용어사전 선언
stopwords = set(STOPWORDS)
stopwords.update(['에 등록된 네이버 페이 구매평','등록된 네이버','에 등록된','페이 구매평','네이버 페이','등록된','네이버구매평','페이','네이버','구매평','너무','진짜','좀','ㅎㅎ','에','다','에'])

#워드클라우드 옵션 세팅
wordcloud = WordCloud(
    font_path='C:\\Users\\COMPUTER\\Desktop\\streamlit_web\\NanumFontSetup_TTF_BARUNGOTHIC\\NanumBarunGothic.ttf',
    width= 1200,
    height=800,
    stopwords=stopwords,
    collocations=False,
)

#메인 함수
def main():
    st.title("Crema")
    with st.form("product_id_form"):
        product_id = st.number_input("product_id", min_value=1, max_value=10000)
        col1, col2 = st.columns([1,1])
        with col1:
            submitted = st.form_submit_button("전체리뷰")
        with col2:
            bad_submitted = st.form_submit_button('악성리뷰')

        df = pd.DataFrame()
        if submitted:
            try:
                st.write("최신 1500건 리뷰 기준입니다.")
                auth_token= st.secrets['crema_token']
                head = {'Authorization': 'Bearer ' + auth_token}
                for i in range (1,15):
                    url = f'https://api.cre.ma/v1/reviews?brand_id=1927&product_code={product_id}&limit=100&date_order_desc=1&page={i}'
                    response = requests.get(url, headers=head)
                    data = response.json()
                    df_temp = pd.DataFrame(data, index=None)
                    df_temp.drop(['id','code','user_name','display', 'user_id', 'user_code', 'product_id', 'review_type','images_count', 'images', 'videos_count', 'video_urls', 'likes_count', 'plus_likes_count', 'comments_count', 'options', 'product_options', 'order_code', 'sub_order_code','source'],axis=1,inplace=True)
                    df = pd.concat([df,df_temp])
                df
            
                #워드클라우드 생성
                text = " ".join(df['message'])
                keyword=wordcloud.generate(text)
                array = keyword.to_array()
                #그래프 작업
                plt.figure(figsize=(10,10))
                plt.imshow(array,
                interpolation="bilinear")
                # plt.savefig("wordcloud.png")
                plt.axis("off")
                #streamlit pyplot 오류 해결
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
            except ValueError:
                st.error('존재하는 상품번호를 입력하세요')

        elif bad_submitted:
            try:
                st.write("결과는 전체리뷰 최근 2000건 기준입니다.")
                auth_token = st.secrets['crema_token']
                head = {'Authorization': 'Bearer ' + auth_token}
                for i in range (1,15):
                    url = f'https://api.cre.ma/v1/reviews?brand_id=1927&product_code={product_id}&limit=100&date_order_desc=1&page={i}'
                    response = requests.get(url, headers=head)
                    data = response.json()
                    df_temp = pd.DataFrame(data, index=None)
                    df_temp.drop(['id','code','user_name','display', 'user_id', 'user_code', 'product_id', 'review_type','images_count', 'images', 'videos_count', 'video_urls', 'likes_count', 'plus_likes_count', 'comments_count', 'options', 'product_options', 'order_code', 'sub_order_code','source'],axis=1,inplace=True)
                    df = pd.concat([df,df_temp])
                df_bad = df.loc[(df['score']<3)]
                df_bad

                #워드클라우드 생성
                text = " ".join(df_bad['message'])
                keyword=wordcloud.generate(text)
                array = keyword.to_array()
                #그래프 작업
                plt.figure(figsize=(10,10))
                plt.imshow(array,
                interpolation="bilinear")
                # plt.savefig("wordcloud.png")
                plt.axis("off")
                #streamlit pyplot 오류 해결
                st.set_option('deprecation.showPyplotGlobalUse', False)
            except ValueError:
                st.error('존재하는 상품번호를 입력하세요')

if __name__ == '__main__':
    main()


# ---Hide streamlit style ---
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)