import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- Configuration ---
TARGET_URL = "https://bukk.it/" 
DOWNLOAD_DIR = "bukkit_archive"
GALLERY_FILE = "directory.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4')

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print(f"Connecting to {TARGET_URL}...")
try:
    response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Failed to connect: {e}")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# Find all links pointing to media files
media_items = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.lower().endswith(VALID_EXTENSIONS):
        # Build absolute URL for downloading, keep relative/filename for the HTML file
        absolute_url = urljoin(TARGET_URL, href)
        filename = os.path.basename(href)
        local_path = os.path.join(DOWNLOAD_DIR, filename)
        media_items.append((absolute_url, local_path, filename))

print(f"Found {len(media_items)} media assets to download.")

# --- Download Phase ---
# SET YOUR TEST LIMIT HERE
TEST_LIMIT = 5 
download_count = 0

for idx, (url, local_path, filename) in enumerate(media_items, 1):
    # Stop processing completely once we hit our test limit
    if download_count >= TEST_LIMIT:
        print(f"\n[TEST MODE] Reached limit of {TEST_LIMIT} downloads. Stopping scraper.")
        break

    if os.path.exists(local_path):
        # Even if the file exists, we count it as part of our test batch
        download_count += 1
        continue
        
    try:
        print(f"[{idx}/{len(media_items)}] Downloading: {filename}")
        img_data = requests.get(url, headers=HEADERS, timeout=10).content
        with open(local_path, 'wb') as handler:
            handler.write(img_data)
        
        download_count += 1 # Increment only after a successful download
        
    except Exception as e:
        print(f"Skipped {filename} due to error: {e}")

# --- Generate the Pictorial Directory ---
print("Building your visual directory file...")

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bukk.it Pictorial Directory</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: #fff; margin: 20px; }
        h1 { text-align: center; color: #aaa; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; padding: 20px; }
        .card { background: #1e1e1e; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: space-between; border: 1px solid #333; }
        .card img, .card video { max-width: 100%; max-height: 180px; object-fit: contain; background: #000; }
        .label { padding: 8px; font-size: 11px; text-align: center; word-break: break-all; color: #999; width: 100%; box-sizing: border-box; background: #171717; }
        a { text-decoration: none; color: inherit; }
    </style>
</head>
<body>
    <h1>Bukk.it Archive Directory</h1>
    <div class="grid">
"""

for url, local_path, filename in media_items:
    # Use the relative path so the directory works on any machine seamlessly
    relative_src = f"{DOWNLOAD_DIR}/{filename}"
    
    if filename.lower().endswith('.mp4'):
        media_tag = f'<video src="{relative_src}" autoplay loop muted playsinline></video>'
    else:
        media_tag = f'<img src="{relative_src}" alt="{filename}" loading="lazy">'
        
    html_content += f"""
        <div class="card">
            <a href="{relative_src}" target="_blank">
                {media_tag}
            </a>
            <div class="label">{filename}</div>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

with open(GALLERY_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Success! Open '{GALLERY_FILE}' in your browser to explore your new pictorial directory.")