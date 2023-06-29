import pandas as pd

# 엑셀 파일 로드
df_order = pd.read_excel('Order.xlsx')
df_account = pd.read_excel('AccountInfo.xlsx', skiprows=3)

# 새로운 열 생성
df_order['check'] = None
df_order['note'] = None

# Order의 모든 행 반복
for i in range(len(df_order)):
    sender = df_order.loc[i, 'Sender']

    # AccountInfo에서 해당 sender 찾기
    df_account_sender = df_account[df_account['기재내용'].str.contains(sender, na=False)]

    # sender가 AccountInfo에 존재하고 금액이 18000원인지 확인
    if not df_account_sender.empty and df_account_sender['맡기신금액'].iloc[0] == 11000:
        df_order.loc[i, 'check'] = 'O'
    else:
        df_order.loc[i, 'check'] = 'X'
        if df_account_sender.empty:
            df_order.loc[i, 'note'] = 'AccountInfo에 sender 정보가 없음'
        elif df_account_sender['맡기신금액'].iloc[0] != 11000:
            df_order.loc[i, 'note'] = '금액이 11000원이 아님'

# 엑셀로 저장
df_order.to_excel('Order_checked.xlsx', index=False)

