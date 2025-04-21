import requests
from bs4 import BeautifulSoup
import time
import os
import html2text
import sys

BASE_URL = "https://lwn.net/Kernel/Index/"
ARTICLE_PREFIX = "https://lwn.net/Articles/"
MARKDOWN_DIR = "./lwn_articles/markdown"
HTML_DIR = "./lwn_articles/html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

# 创建保存目录
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(MARKDOWN_DIR, exist_ok=True)

# 获取Index页面
def fetch_index_page():
    response = requests.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    return response.text

# 解析页面中所有以https://lwn.net/Articles/开头的链接
def extract_article_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/Articles/'):
            full_url = f"https://lwn.net{href}"
            links.add(full_url.rstrip('/ '))
        elif href.startswith(ARTICLE_PREFIX):
            links.add(href.rstrip('/ '))
    return list(links)  # 只取前10个链接用于测试

# 下载HTML页面
def download_articles(urls):
    for i, url in enumerate(urls):
        article_id = url.split('/')[-1].strip()
        html_path = os.path.abspath(os.path.join(HTML_DIR, f"{article_id}.html"))

        # 如果文件已存在，则跳过
        if os.path.exists(html_path):
            print(f"[{i+1}/{len(urls)}] Skipping {url} (already downloaded)")
            continue

        retry = 3

        while (retry != 0):
            try:
                print(f"[{i+1}/{len(urls)}] Downloading {url} ...")
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print('Saved.')

                print('Wait for 10s...')
                time.sleep(10)  # 礼貌性延时，避免被屏蔽
                retry = 0

            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                retry = retry - 1
                if retry == 0:
                    print('WARNING: Max retries exceeded, skip this article.')
                    continue
                else:
                    print('sleep 30s to retry')
                    time.sleep(30)

# 从HTML目录中生成Markdown文件
def parse_articles():
    for filename in os.listdir(HTML_DIR):

        if not filename.endswith(".html"):
            continue

        article_id = os.path.splitext(filename)[0]
        html_path = os.path.join(HTML_DIR, filename)
        markdown_path = os.path.join(MARKDOWN_DIR, f"{article_id}.md")

        print('Parsing %s... ' % html_path, end='')

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            title_tag = soup.find('title')
            article_div = soup.find('div', class_='ArticleText')

            title = title_tag.get_text(strip=True) if title_tag else 'No Title'
            html_body = str(article_div) if article_div else '<p>No Content</p>'

            markdown_converter = html2text.HTML2Text()
            markdown_converter.ignore_links = False
            markdown_converter.ignore_images = False
            markdown_converter.body_width = 0

            content_md = markdown_converter.handle(html_body)

            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n{content_md}")
            print('OK')

        except Exception as e:
            print(f"Failed to parse {filename}: {e}")

# 主函数
def main():

    if len(sys.argv) <= 1 or sys.argv[1] != '--no-fetch':
        index_html = fetch_index_page()
        article_links = extract_article_links(index_html)
        print(f"Found {len(article_links)} article links.")
        download_articles(article_links)
        parse_articles()
    else:
        print("Running in --no-fetch mode: only parsing HTML to Markdown...")
        parse_articles()

if __name__ == "__main__":
    main()
