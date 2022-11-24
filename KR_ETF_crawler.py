import pandas as pd

# print("pandas version: ", pd.__version__)
# Pandas User Configuration
pd.set_option('display.max_rows', 500) # 최대 줄 수 설정
pd.set_option('display.max_columns', 5000) # 최대 열 수 설정
pd.set_option('display.width', 5000) # 표시할 가로의 길이

df = pd.read_csv('KRX_ETF_전종목기본정보.csv', encoding='cp949')
df['단축코드'] = df['단축코드'].astype(str)

columns = ['단축코드','한글종목명','지수산출기관', '상장일','상장좌수', '총보수']

while True:
    search_type = input('원하시는 검색 조건을 선택하세요\n1: 종목번호 2: 종목명 3: 기초자산분류:(숫자만 입력) ')
    df_search_simple = None
    if search_type == str(1):
        search_input = input('종목번호를 입력하세요(다중입력은 콤마(,)로 구분하여 입력: ')
        print('\n----------------------------------------------------------------------------------')
        search_input = str(search_input.replace(' ','')) # 공백 입력시 공백삭제
        search_input = str(search_input.replace(',','|')) # 콤마(,)를 OR 조건 연산자(|)로 변경
        # 검색결과
        df_search = df.loc[df['단축코드'].str.contains(search_input)].sort_values(by='상장일')
        df_search_simple = df_search[columns]
    elif search_type == str(2):
        search_input = input('종목명을 입력하세요(다중입력은 콤마(,)로 구분하여 입력): ')
        print('\n----------------------------------------------------------------------------------')
        search_input = str(search_input.replace(' ','')) # 공백 입력시 공백삭제
        search_input = str(search_input.replace(',','|')) # 콤마(,)를 OR 조건 연산자(|)로 변경
        # 검색결과
        search_input3 = input('정렬조건을 입력하세요(0: 상장일, 1:상장좌수:) ')
        if search_input3 == str(0):
            df_search = df.loc[df['한글종목명'].str.contains(search_input)].sort_values(by='상장일')
        elif search_input3 == str(1):
            df_search = df.loc[df['한글종목명'].str.contains(search_input)].sort_values(by='상장좌수', ascending=False)
        df_search_simple = df_search[columns]
    elif search_type == str(3):
        input_list = df['기초자산분류'].unique()
        dict_input_list = {string:idx for idx, string in enumerate(input_list)}
        print(dict_input_list)
        search_input2 = input('기초자산분류를 선택하세요:')
        print('\n----------------------------------------------------------------------------------')
        for key, value in dict_input_list.items():
            if search_input2 == str(value):
                search_input3 = input('정렬조건을 입력하세요(0: 상장일, 1:상장좌수): ')
                if search_input3 == str(0):
                    df_search = df.loc[df['기초자산분류'].str.contains(key)].sort_values(by='상장일')
                elif search_input3 == str(1):
                    df_search = df.loc[df['기초자산분류'].str.contains(key)].sort_values(by='상장좌수', ascending=False)
                df_search_simple = df_search[columns]
                break

    print(df_search_simple.head(30))
    print('\n----------------------------------------------------------------------------------\n')