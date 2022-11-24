# FinanceDataReader 
df_fdr = fdr.DataReader(str(ticker))
df_fdr.reset_index(inplace=True)

df_fdr.rename(columns={'Date':'index', 'Close':'close_fdr'}, inplace=True)
df_fdr = df_fdr[['index','close_fdr']]

df_fdr['index'] = df_fdr['index'].astype(str)
df_fdr['index'] = df_fdr['index'].apply(lambda x: str(x).replace('-',''))

df_fdr['ticker_fdr'] = 'FDR'

df_fdr.head()

# KRX정보데이터시스템
etf_base_info = pd.read_csv('./data/ETF/KRX_ETF_전종목기본정보.csv', encoding='cp949')
ticker_reg = datetime.strptime(etf_base_info.loc[etf_base_info['단축코드']==ticker, '상장일'].values[0], "%Y/%m/%d").date()
ticker_name = etf_base_info.loc[etf_base_info['단축코드']==ticker, '한글종목약명'].values[0]
print(ticker_reg, ticker, ticker_name)
start = str(ticker_reg)
end = str(date.today())


my_ticker = ["ETF"] 
periods = pd.period_range(start=start,end=end, freq='D')

# 임시데이터 저장 리스트
temp_list = []

# 코인 종류별, 월별 데이터 모으는 작업
for _ticker in my_ticker:
    for pr in tqdm(periods):
        try:
            year_month = str(pr).replace('-','')
            fileName = '{}.csv'.format(year_month)
            # print(ticker, './data/'+ ticker + '/' + str(pr.year) + '/' + fileName)
            df = pd.read_csv('./data/'+ _ticker + '/' + str(pr.year) + '/' + fileName, encoding='cp949')
            df['ticker'] = _ticker
            df['index'] = year_month
            temp_list.append(df)
        except Exception as e:
            print(e)
            pass

df = pd.concat(temp_list, axis=0)

df.rename(columns={'시가':'open','고가':'high','저가':'low','종가':'close_krx','거래량':'volume'}, inplace=True)
# 단독 ticker일 때,
# df.fillna(method='ffill', inplace=True)
# 다중 ticker일 때,
df_krx = df[df['종목코드']==ticker].fillna(method='ffill')
df_krx = df_krx[['index','close_krx']]
df_krx['close_krx'] = df_krx['close_krx'].astype(int)
df_krx['ticker_krx'] = 'KRX'

df_krx.head()

# FDR & KRX 데이터 merge

df = pd.merge(df_fdr, df_krx, on='index', how='left')
df.head()

fig = go.Figure()

fig.add_trace(
    go.Scatter(x=df['index'], y=df['close_fdr'],
               mode='lines',
               name='FDR'),
)
fig.add_trace(
    go.Scatter(x=df['index'], y=df['close_krx'],
               mode='lines',
               name='KRX'),
)

fig.update_layout(
 legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
)

# x축 데이터 없는 시간은 미표출
fig.update_xaxes(
    type='category',
    nticks=20
)