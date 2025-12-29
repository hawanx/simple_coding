import praw

def get_followed_subs(client_id, client_secret, username, password, user_agent):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )
    return reddit, set(sub.display_name.lower() for sub in reddit.user.subreddits(limit=None))

# ---- Fill these for both users ----
user1_creds = {
    "client_id":  '72mhHwhQb-ibJywqtlnjVQ',
    "client_secret": '-93kdb_J4VcQowVbASbAkzUuG9fecA',
    "username": 'thakgayahuvrolyfse2',
    "password": 'sanjay67',
    "user_agent": 'channel_fetcher by u/thakgayahuvrolyfse2',
}


# ---- Get subreddits for both users ----
_, subs_user1 = get_followed_subs(**user1_creds)

for sub in subs_user1:
    print(f"Subscribing to r/{sub}")

