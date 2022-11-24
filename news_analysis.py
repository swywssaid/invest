# 한국언론지능재단에서 한국의 모든 언론사로부터 뉴스데이터 가져오는 api 제공 (광고 없음)
# 데이터 다운로드/관계도 분석/키워드 트랜드/연관어 분석/정보 추출
# https://www.bigkinds.or.kr/
# 
# #코랩에서 한글 사용하기
# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf
# !pip install konlpy
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('여기에 데이터가 들어있는 경로와 파일명 입력하세요!')

#엑셀파일에서 '본문' 내용만 추출하기
text = data['본문']
change = list(map(str, text))
text2 = ", ".join(change)

#'본문'에서 '명사'만 추출하기
okt = Okt()
extract = okt.nouns(text2)

#명사 리스트에서 1글자를 넘는 단어만 고르기
noun_list = []

for n in extract:
    if len(n) >1:
        noun_list.append(n)

#추출한 명사가 몇개인지 세기
counts = Counter(noun_list)

#상위 100개 단어 목록 만들기
tags = counts.most_common(100)

#워드 클라우드 생성하기
wc = WordCloud(font_path='여기에 폰트파일이 들어있는 경로와 파일명 입력하세요!', 
               background_color="white", 
               max_font_size=200,
               width = 800,
               height =800)
cloud = wc.generate_from_frequencies(dict(tags))

#워드 클라우드 그리기
plt.figure(figsize=(10, 10))
plt.axis('off')
plt.imshow(cloud)
plt.show()