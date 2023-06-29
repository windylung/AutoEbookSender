import pandas as pd
import faker

# faker library to generate fake data
fake = faker.Faker('ko_KR')

data = {
    'Name': [fake.name() for _ in range(50)],
    'Comment': [f"{fake.name()} / {fake.safe_email()}" for _ in range(50)],
    'Date': [fake.date(pattern="%Y-%m-%d", end_datetime=None) for _ in range(50)],
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('comments.xlsx', index=False)
