import logging
import requests
import urllib
import re
import os
import datetime

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}


def download_img(url, path, cookie=None, session: requests.session = None):
    url = url.strip()
    urlparse = urllib.parse.urlparse(url)
    if urlparse.scheme == "":
        urlparse = urlparse._replace(scheme='https')
        url = urllib.parse.urlunparse(urlparse)
    if session:
        response = session.get(url)
    else:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }
        if cookie != None:
            header["Cookie"] = cookie
        response = requests.get(url, headers=header)
    assert response.status_code == 200
    with open(path, "wb") as f:
        f.write(response.content)


def get_img_url(docs_html_path):
    with open(docs_html_path, encoding='utf') as f:
        pattern = re.compile(r"https://cn.bing.com/th\?id=(.*?)\.jpg")
        result = pattern.findall(f.read())
        logging.debug(result)
        return result


def months_between(start_month, end_month):
    """返回包含起止月份的月份列表。

    支持的输入格式："YYYY-MM" 或 "YYYYMM"（字符串），
    也支持 (year, month) 的元组/列表输入。

    返回格式为 'YYYY-MM' 的字符串列表，按时间升序。
    """
    def _parse(m):
        if isinstance(m, (list, tuple)):
            y, mo = int(m[0]), int(m[1])
            return y, mo
        if isinstance(m, str):
            s = m.strip()
            if '-' in s:
                parts = s.split('-', 1)
                return int(parts[0]), int(parts[1])
            if len(s) == 6 and s.isdigit():
                return int(s[:4]), int(s[4:6])
            raise ValueError("月份字符串格式应为 'YYYY-MM' 或 'YYYYMM'")
        raise TypeError("不支持的月份输入类型")

    sy, sm = _parse(start_month)
    ey, em = _parse(end_month)

    start_index = sy * 12 + (sm - 1)
    end_index = ey * 12 + (em - 1)
    if start_index > end_index:
        # 统一返回升序范围
        start_index, end_index = end_index, start_index

    months = []
    for idx in range(start_index, end_index + 1):
        y = idx // 12
        m = idx % 12 + 1
        months.append(f"{y}-{m:02d}")
    return months


def main():
    logging.basicConfig(level=logging.INFO)
    '''
    img_list = []
    for i in months_between("2025-05", "2026-01"):
        img_list.extend(get_img_url("docs/{}.html".format(i)))
    img_list = list(set(img_list))
    with open("1.txt", "w", encoding='utf') as f:
        for i in img_list:
            f.write("https://cn.bing.com/th?id={}.jpg\n".format(i))
    '''
    with open("1.txt", encoding='utf') as f:
        with requests.session() as s:
            s.headers.update(header)
            path = "img"
            os.makedirs(path, exist_ok=True)
            for url in f:
                img_name = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)[
                    "id"][0].replace("OHR.", "").replace("_UHD", "")
                img_path = os.path.join(path, img_name)
                logging.info(img_path)
                download_img(url, img_path, session=s)

    pass


if __name__ == "__main__":
    main()
