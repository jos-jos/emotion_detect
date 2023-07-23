import os
import torch
from torchtext.data import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torchtext import transforms as T
from torch.utils.data import TensorDataset


# 读取数据集，进行分词，并返回分词后的影评和数字标签
# def read_imdb(path='/home/previous/work/nlp/TextCNN/data/train/IMDB_Dataset.csv', split=0.8):
# def read_imdb(path='./datasets/IMDB_Dataset.csv', split=0.8):
def read_imdb(path='./datasets/tweet_emotions.csv', split=0.8):
    '''
    reviews, labels = [], []
    # 创建分词器
    tokenizer = get_tokenizer('basic_english')
    for label in ['pos', 'neg']:
        folder_name = os.path.join(path, 'train' if is_train else 'test', label)
        for filename in os.listdir(folder_name):
            with open(os.path.join(folder_name, filename), mode='r', encoding='utf-8') as f:
                reviews.append(tokenizer(f.read()))
                labels.append(1 if label == 'pos' else 0)
    return reviews, labels
    '''
    # label_map = { "positive" : 1 , "negative" : 0 }
    label_map = { "neutral" : 0 , "worry" : 1 , "happiness" : 2 , "sadness" : 3, "love" : 4, "surprise" : 5, "fun" : 6, "relief" : 7, "hate" : 8 ,"empty" : 9, "enthusiasm" : 10, "boredom" : 11, "anger" : 12}
    tokenizer = get_tokenizer('basic_english')
    with open(path, "r") as f:
        # texts = [[tokenizer(i.rsplit(",", 1)[0][1:-1]), label_map[i.rsplit(",", 1)[1].replace("\n", "")]] for i in f.readlines()[1:]]
        texts = [[tokenizer(i.split(",", 2)[2].replace("\n", "").replace("\"" , "")), label_map[i.split(",", 2)[1]]] for i in f.readlines()[1:]]
    split_num = int(len(texts)*split)
    train_sets = texts[:split_num]
    test_sets = texts[split_num:]
    train_review = [i[0] for i in train_sets]
    train_label = [i[1] for i in train_sets]
    test_review = [i[0] for i in test_sets]
    test_label = [i[1] for i in test_sets]
    return train_review, train_label, test_review, test_label

# 对数据集中句子的单词长度进行统一
def build_dataset(reviews, labels, vocab, max_len=512):
    text_transform = T.Sequential(
        T.VocabTransform(vocab=vocab),
        T.Truncate(max_seq_len=max_len),
        T.ToTensor(padding_value=vocab['<pad>']),
        T.PadTransform(max_length=max_len, pad_value=vocab['<pad>']),
    )
    dataset = TensorDataset(text_transform(reviews), torch.tensor(labels))
    return dataset


def load_imdb():
    reviews_train, labels_train, reviews_test, labels_test = read_imdb()
    # 创建词汇字典，输入需为可迭代对象
    vocab = build_vocab_from_iterator(reviews_train, min_freq=3, specials=['<pad>', '<unk>'])
    vocab.set_default_index(vocab['<unk>'])

    train_data = build_dataset(reviews_train, labels_train, vocab)
    test_data = build_dataset(reviews_test, labels_test, vocab)
    return train_data, test_data, vocab

"""
对于字典vocab

    查看字典（列表形式）
    print(vocab.get_itos())
    例：
     ['<unk>', 'cat', 'The', 'dog', 'ball', 'kidding', 'like']

    查看字典（字典形式），对应词的索引
    print(vocab.get_stoi())
    例：
    {'dog': 3,'<unk>': 0, 'kidding': 5, 'cat': 1, 'ball': 4}
"""
