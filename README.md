reference文件夾放在source裏面

直接運行main.py即可

使用 [BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) 模型（沒有微調）

preprocessing：先讀取一次pdf的資料並保存成json檔案，加速之後讀取的速度

model: 加載模型和計算的代碼