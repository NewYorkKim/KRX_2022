import pandas as pd
from konlpy.tag import Okt
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from konlpy.tag import Hannanum
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import MaxScoreTokenizer

class preprocesser:
    def __init__(self) -> None:
        pass

    def load_data(self,file_path): # 데이터 불러오기, 불필요한 열 삭제, null값 삭제.
        df = pd.read_csv(file_path)
        df2 = df.drop(["Unnamed: 0"],axis=1)
        df3 = df2.dropna(axis=0)
        return df3

    def clean_text(self,title):
        text_rmv = re.sub('[-=+,#/\?:^.@*\"※%~∼ㆍ!【】』㈜©囹圄秋 ■◆◇▷▶◁◀ △▲▽▼<>‘|\(\)\[\]`\'…》→←↑↓↔〓♤♠♡♥♧♣⊙◈▣◐◑☆★\”\“\’·※~ ! @ # $ % ^ & * \ " ]', ' ', title)
        text_rmv = ' '.join(text_rmv.split())
        return text_rmv

    def make_corpus(self,file_path):
        corpus = DoublespaceLineCorpus(file_path,iter_sent=True)
        word_extractor = WordExtractor()
        word_extractor.train(corpus)
        word_score = word_extractor.extract()
        scores = {word:score.cohesion_forward for word, score in word_score.items()}
        return scores

    def get_nouns(self, scores, text): # text는 문장이 들어가야함.
        maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
        text = self.clean_text(text)
        text = maxscore_tokenizer.tokenize(text)
        return text

    def make_list_to_str(self, lst):
        return " ".join(lst)

    def prep(self, corpus ,df, title = True, tokenizing = True, save = False):
        if title:
            data = df["기사제목"]
            name = "title"
        else:
            data = df["본문"]
            name = "news"
        scores = corpus
        all_data = []
        for str in data:
            text = self.get_nouns(scores, str)
            if tokenizing:
                all_data.append(text2)
            else:
                text2 = self.make_list_to_str(text)
                all_data.append(text2)
        if save:
            outputFileName = "preprocessed " + name
            dd = pd.DataFrame(all_data)
            dd.to_csv("data/" + outputFileName)
        else:
            return all_data

    def select_category(self, df, category):
        data = []
        for i in range(len(df)):
            if df.iloc[i].카테고리 == category:
                data.append(df.iloc[i])
        dataframe = pd.DataFrame(data,columns=['카테고리', '언론사', '기사제목', '날짜', '본문',"기사링크"])
        return dataframe

    def remove_stop_words(self):
        pass