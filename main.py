import json
from tqdm import tqdm
from model.retrieval import retrieve
from preprocess.preprocess import save_data

source_path = 'source/'
question_path = 'questions_preliminary.json'
save_path = 'answer.json'

# 讀取數據並保存到json（若已預先讀取可以注釋掉這段
# print('讀取資料中')
# save_data(source_path, source_path)
# print('資料已保存')

# 讀取參考資料文件
print('讀取預讀取資料中')
with open(source_path+'finance_data.json', 'rb') as f_s:
    key_to_source_dict = json.load(f_s) 
    corpus_dict_finance = {int(key): value for key, value in key_to_source_dict.items()}

with open(source_path+ 'insurance_data.json', 'rb') as f_s:
    key_to_source_dict = json.load(f_s) 
    corpus_dict_insurance = {int(key): value for key, value in key_to_source_dict.items()}

with open(source_path+'/reference/faq/pid_map_content.json', 'rb') as f_s:
    key_to_source_dict = json.load(f_s)
    corpus_dict_faq = {int(key): value for key, value in key_to_source_dict.items()}

# 初始化字典
print('初始化答案')
answer_dict = {"answers": []} 

# 讀取問題檔案
print('讀取問題')
with open(question_path, 'rb') as f:
    qs_ref = json.load(f)  

# 回答問題
print('檢索答案中')
for q_dict in tqdm(qs_ref['questions']):
  if q_dict['category'] == 'finance':
    retrived = retrieve(q_dict['query'], q_dict['source'], corpus_dict_finance)
    answer_dict['answers'].append({'qid': q_dict['qid'], 'retrieve': retrived})
  elif q_dict['category'] == 'insurance':
    retrived = retrieve(q_dict['query'], q_dict['source'], corpus_dict_insurance)
    answer_dict['answers'].append({'qid': q_dict['qid'], 'retrieve': retrived})
  elif q_dict['category'] == 'faq':
    faq_dict = {key: str(value) for key, value in corpus_dict_faq.items() if key in q_dict['source']}
    retrived = retrieve(q_dict['query'], q_dict['source'], faq_dict)
    answer_dict['answers'].append({'qid': q_dict['qid'], 'retrieve': retrived})
  else:
    raise ValueError('Invalid category')
print('檢索完畢')
# 保存答案

print('保存答案')
with open(save_path, 'w') as f:
  json.dump(answer_dict, f, ensure_ascii=False, indent=4)