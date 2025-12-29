import asyncio
from playwright.async_api import async_playwright

async def scrape_instagram_posts(profile_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Opening:", profile_url)
        await page.goto(profile_url, wait_until="networkidle")

        # Scroll and collect post URLs
        post_links = set()
        prev_height = 0

        while len(post_links) < 50:
            # Extract post URLs
            links = await page.locator("a[href*='/p/']").evaluate_all("elements => elements.map(e => e.href)")
            post_links.update(links)

            if len(post_links) >= 50:
                break

            # Scroll down
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1500)

            # Stop if no more scroll
            height = await page.evaluate("document.body.scrollHeight")
            if height == prev_height:
                break
            prev_height = height

        post_links = list(post_links)[:50]
        print(f"Found {len(post_links)} posts")

        total_likes = 0
        total_comments = 0

        for i, post_url in enumerate(post_links, start=1):
            print(f"Opening post {i}: {post_url}")
            await page.goto(post_url, wait_until="networkidle")
            await page.wait_for_timeout(1200)

            # Extract likes (for image posts)
            likes = 0
            comments = 0

            try:
                likes_text = await page.locator("section span span").first.text_content()
                likes = int(likes_text.replace(",", "").replace(" likes", "").strip())
            except:
                pass

            # Extract comments
            try:
                comments = await page.locator("ul ul").count()
            except:
                comments = 0

            total_likes += likes
            total_comments += comments

        avg_likes = round(total_likes / len(post_links), 2)
        avg_comments = round(total_comments / len(post_links), 2)

        print("\n--- Final Stats ---")
        print(f"Total Likes: {total_likes}")
        print(f"Average Likes: {avg_likes}")
        print(f"Total Comments: {total_comments}")
        print(f"Average Comments: {avg_comments}")

        await browser.close()

# ------------------------------
# Run the scraping
# ------------------------------

profile_url = "https://www.instagram.com/nike/"  # change here
asyncio.run(scrape_instagram_posts(profile_url))
