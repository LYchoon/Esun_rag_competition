import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def retrieve(query, source, corpus):
    """
    input: query, source, corpus
    output: source (which get highest scores)
    """

    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
    model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-v2-m3")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()

    answer = ''
    best_scores = -float('inf')
    max_length = 2048 # best parameters in [1024, 2048, 4096, 8192]
    for s in source:
        inputs = tokenizer(query, corpus[int(s)], return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        score = outputs.logits.squeeze().item()
        if score > best_scores:
            answer = s
    return answer