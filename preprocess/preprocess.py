import os
import json
from tqdm import tqdm
import pdfplumber

def read_pdf(file_path):
    """Read pdf and return text without \\n"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.replace('\n', '')

def load_data(source_path):
    """
    input: path
    output: dict (key:filename, value:pdf's content)
    """
    masked_file_ls = os.listdir(source_path)
    corpus_dict = {}
    for file in tqdm(masked_file_ls):
        file_id = int(file.replace('.pdf', ''))
        text = read_pdf(os.path.join(source_path, file))
        corpus_dict[file_id] = text
    return corpus_dict

def save_data(source_path, save_path):
    """read data in source_path and save in save_path"""
    source_path_insurance = os.path.join(source_path, 'reference/insurance')  # 設定參考資料路徑
    corpus_dict_insurance = load_data(source_path_insurance)

    source_path_finance = os.path.join(source_path, 'reference/finance')  # 設定參考資料路徑
    corpus_dict_finance = load_data(source_path_finance)

    with open(save_path+'finance_data.json', 'w', encoding='utf8') as f:
            json.dump(corpus_dict_finance, f, ensure_ascii=False, indent=4)  # 儲存檔案，確保格式和非ASCII字符

    with open(save_path+'insurance_data.json', 'w', encoding='utf8') as f:
            json.dump(corpus_dict_insurance, f, ensure_ascii=False, indent=4)  # 儲存檔案，確保格式和非ASCII字符
