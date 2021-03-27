import os
import urllib.request
import zipfile
import re


def download_from_url(url, save_path=''):
    if os.path.exists(save_path):
        print('The file already exists.')
    else:
        urllib.request.urlretrieve(url, save_path)


def unzip_file(zip_file):
    with zipfile.ZipFile(zip_file) as z:
        z.extractall()  # カレントディレクトリに保存


def obtain_str_fromtxt(txtfile_path, encoding):
    with open(txtfile_path, 'r', encoding=encoding) as f:
        text = f.read()
    return text


def clean_text(raw_text):
    """
    生テキストからルビ等を除去する．
    """
    # "."は任意の位置文字，"+?"は直前文字の一回以上の繰り返しに最短一致
    text = re.sub(r'《.+?》', '', raw_text)  # ルビの除去
    text = re.sub(r'｜', '', text)  # ルビの始まり記号を除去
    # "*?"は直前文字の一回以上の繰り返しに最短一致
    text = re.sub(r'［＃.*?］', '', text)  # 入力者注を除去
    text = re.sub(r'---[\s\S]*---', '', text)  # ヘッダーを除去
    text = re.sub(r'\n+', '\n', text)  # 無駄に改行しているものを減らす
    text = re.sub(r'　', ' ', text)  # 全角スペースを半角に変換
    text = re.split(r'底本：', text)[0]  # "底本"以下を除去
    text = text.strip()  # 両端の連続する空白文字を除去

    return text


def prepare_karatxt(url='https://www.aozora.gr.jp/cards/000363/'
                    + 'files/42286_ruby_36920.zip'):

    download_from_url(url)  # zipファイルのダウンロード
    zip_file = ''
    for f in os.listdir('./'):
        if f.endswith('.zip'):
            zip_file = f
            break
    unzip_file(zip_file)  # zipファイルの展開

    # zipを展開して得られる，txtファイルのパスを取得
    txtfile_path = ''
    for f in os.listdir('./'):
        if f.endswith('.txt'):
            txtfile_path = f
            break

    assert len(txtfile_path) != 0, 'Getting the Karamazov text was failed.'

    # テキストの読み込み&整形
    raw_text = obtain_str_fromtxt(txtfile_path, encoding='SJIS')
    cleansed_text = clean_text(raw_text)

    return cleansed_text
