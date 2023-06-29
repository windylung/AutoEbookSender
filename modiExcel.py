import pandas as pd

# 1. 기존 엑셀 파일 이름은 comments
df = pd.read_excel('comments.xlsx')

# 2. Comment 열을 수정
# 3. Comment 열의 내용을 / 을 기준으로 나누어서 각각 sender와 email로 열을 새롭게 추가해서 데이터를 넣어줘
df[['Sender', 'Email']] = df['Comment'].str.split('/', expand=True)

# 4. 각 데이터 양쪽에 공백이 있을 경우 제거해줘
df['Sender'] = df['Sender'].str.strip()
df['Email'] = df['Email'].str.strip()

# 5. 모든 행을 다음과 같이 수정한 뒤 Order 이름의 엑셀로 저장해줘
df.to_excel('Order.xlsx', index=False)
