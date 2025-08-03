import pandas as pd
import numpy as np

n_users = 10000
start_date = pd.to_datetime("2025-01-01")
end_date = pd.to_datetime("2025-06-30")
channels = ["Paid Ads", "Organic", "Referral"]
channel_probs = [0.5, 0.3, 0.2]

users = pd.DataFrame({
    "user_id": np.arange(10001, 10001 + n_users),
    "signup_date": pd.to_datetime(np.random.choice(pd.date_range(start_date, end_date), size=n_users)),
    "acquisition_channel": np.random.choice(channels, size=n_users, p=channel_probs)
})
users.to_csv("users.csv", index=False)

events_list = []
event_types = ["login", "workout", "message_coach", "share", "browse"]

for _, row in users.iterrows():
    n_events = np.random.poisson(lam=10)  # average 10 events/user
    if n_events == 0:
        continue
    event_dates = np.random.choice(
        pd.date_range(row.signup_date, end_date, freq='H'),
        size=n_events
    )
    for d in event_dates:
        events_list.append({
            "user_id": row["user_id"],
            "event_type": np.random.choice(event_types),
            "timestamp": d
        })

events_df = pd.DataFrame(events_list)
events_df.to_csv("events.csv", index=False)

paying_users = users.sample(frac=0.15, random_state=42)  # 15% conversion
plan_types = ["Monthly", "Quarterly"]
payments = []

for _, row in paying_users.iterrows():
    plan = np.random.choice(plan_types)
    amount = 10 if plan == "Monthly" else 30
    payment_date = row.signup_date + pd.Timedelta(days=np.random.randint(1, 30))
    if payment_date > end_date:
        continue
    payments.append({
        "user_id": row["user_id"],
        "amount": amount,
        "payment_date": payment_date,
        "plan_type": plan
    })

payments_df = pd.DataFrame(payments)
payments_df.to_csv("payments.csv", index=False)
