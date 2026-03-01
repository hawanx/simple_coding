import json
import os
import webbrowser
from datetime import datetime

file_path = r"C:\Users\Samratt\Desktop\u_femcelgod3_posts.jsonl"   # ← FILE PATH DAALO


def format_time(timestamp):
    try:
        return datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Unknown"


def extract_image(row):
    url = row.get("url_overridden_by_dest") or row.get("url")
    if isinstance(url, str) and url.endswith((".jpg", ".jpeg", ".png", ".webp")):
        return url

    preview = row.get("preview")
    if preview and "images" in preview:
        try:
            return preview["images"][0]["source"]["url"].replace("&amp;", "&")
        except:
            pass

    thumbnail = row.get("thumbnail")
    if isinstance(thumbnail, str) and thumbnail.startswith("http"):
        return thumbnail

    return None


def main():
    posts = []
    subreddits = set()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
                posts.append(row)
                if "subreddit" in row:
                    subreddits.add(row["subreddit"])
            except:
                continue

    html_content = generate_html(posts, sorted(subreddits))

    output_file = "reddit_viewer.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    webbrowser.open("file://" + os.path.realpath(output_file))


def generate_html(posts, subreddit_list):

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Reddit Viewer</title>
<style>
body {
    background:#0f0f0f;
    font-family:Arial;
    color:#d7dadc;
    margin:0;
    display:flex;
}

.sidebar {
    width:250px;
    background:#141414;
    padding:20px;
    border-right:1px solid #343536;
    height:100vh;
    overflow-y:auto;
    position:fixed;
}

.sidebar h2 {
    margin-top:0;
    font-size:18px;
}

.sidebar ul {
    list-style:none;
    padding:0;
}

.sidebar li {
    margin-bottom:8px;
    color:#4fbcff;
}

.main {
    margin-left:270px;
    width:100%;
    padding:30px;
}

.sort-bar {
    text-align:center;
    margin-bottom:20px;
}

button {
    padding:8px 14px;
    background:#ff4500;
    color:white;
    border:none;
    border-radius:5px;
    cursor:pointer;
}

.post {
    background:#1a1a1b;
    padding:18px;
    margin-bottom:18px;
    border-radius:8px;
    border:1px solid #343536;
}

.post:hover {
    border-color:#818384;
}

.header {
    font-size:13px;
    color:#818384;
}

.subreddit {
    color:#4fbcff;
    font-weight:bold;
}

.author {
    color:#ff4500;
}

.date {
    color:#aaa;
}

.title {
    font-size:20px;
    margin:10px 0;
    font-weight:bold;
}

.body {
    font-size:14px;
    margin-top:6px;
    line-height:1.5;
    white-space:pre-wrap;
}

.footer {
    margin-top:12px;
    font-size:13px;
    color:#818384;
    display:flex;
    gap:20px;
}

img {
    max-width:100%;
    margin-top:12px;
    border-radius:6px;
}

a.button {
    display:inline-block;
    margin-top:10px;
    padding:6px 12px;
    background:#ff4500;
    color:white;
    text-decoration:none;
    border-radius:5px;
    font-size:13px;
}
</style>
</head>
<body>

<div class="sidebar">
    <h2>Subreddits</h2>
    <ul>
"""

    # Sidebar subreddit list
    for sub in subreddit_list:
        html += f"<li>r/{sub}</li>"

    html += """
    </ul>
</div>

<div class="main">

<div class="sort-bar">
    <button onclick="toggleSort()">Toggle Sort (Newest ⇅ Oldest)</button>
</div>

<div id="posts">
"""

    # Posts
    for row in posts:
        subreddit = row.get("subreddit", "unknown")
        author = row.get("author", "unknown")
        created_raw = row.get("created_utc", 0)
        created = format_time(created_raw)
        score = row.get("score", 0)
        comments = row.get("num_comments", 0)
        title = row.get("title", "")
        body = row.get("selftext", row.get("body", ""))
        permalink = row.get("permalink", "")
        reddit_url = f"https://www.reddit.com{permalink}" if permalink else "#"

        image_url = extract_image(row)
        image_html = f'<img src="{image_url}">' if image_url else ""

        html += f"""
<div class="post" data-time="{created_raw}">
    <div class="header">
        <span class="subreddit">r/{subreddit}</span> • 
        <span class="author">u/{author}</span> • 
        <span class="date">{created}</span>
    </div>

    <div class="title">{title}</div>
    <div class="body">{body}</div>

    {image_html}

    <a class="button" href="{reddit_url}" target="_blank">
        Open on Reddit
    </a>

    <div class="footer">
        ⬆ {score} | 💬 {comments}
    </div>
</div>
"""

    html += """
</div>

<script>
let newestFirst = true;

function toggleSort() {
    const container = document.getElementById("posts");
    const posts = Array.from(container.getElementsByClassName("post"));

    posts.sort((a, b) => {
        const timeA = parseInt(a.dataset.time);
        const timeB = parseInt(b.dataset.time);
        return newestFirst ? timeA - timeB : timeB - timeA;
    });

    newestFirst = !newestFirst;
    posts.forEach(post => container.appendChild(post));
}
</script>

</div>
</body>
</html>
"""

    return html


if __name__ == "__main__":
    main()