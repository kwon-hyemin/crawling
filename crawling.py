from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
import re
import pandas as pd
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from icecream import ic
import nltk

from context.domains import File, Reader

'''
문장 형태의 문자 데이터를 전처리할 때 많이 사용되는 방법이다. 
말뭉치(코퍼스 corpus)를 어떤 토큰의 단위로 분할하냐에 따라 #Interval
단어 집합의 크기, 단어 집합이 표현하는 토크의 형태가 다르게 나타나며 
이는 모델의 성능을 좌지우지하기도 한다. 

이때 텍스트를 토큰의 단위로 분할하는 작업을 토큰화라고 한다. (토큰요소 코퍼스의 단위)  word
토큰의 단위는 보통 의미를 가지는 최소 의미 단위로 선정되며, 단락 \n 의 
토큰의 단위를 단어로 잡으면 Word Tokenization이라고 하고, 
문장으로 잡으면 Sentence Tokeniazation이라고 한다. 
영어는 주로 띄어쓰기 기준으로 나누고, 
한글은 단어 안의 형태소를 최소 의미 단위로 인식해 적용한다.
형태소(形態素, 영어: morpheme)는 언어학에서 의미가 있는 가장 작은 말의 단위이다. 모프

형태소는 의미가 있는 워드  코퍼스는 텍스트의 집합
워드 스페이스바 or 엔터로 나누어져있음 - 형태소가 결합된 상태 (아침에)
형태소 의미가 있는 워드 (아침 - 실질 형태소/ 에 - 형식 형태소)
형태소는 실질형태소  
형식형태소는  날려버려야한다 

텍스트는 워드와 센텐스로 이루어져있음 

코퍼스(영어: corpus) 말뭉치는 언어학에서 주로 구조를 이루고 있는 텍스트 집합이다.
코퍼스(corpus)는 단어들을 포함한다.
임베딩(embedding)은 변환한 벡터들이 위치한 공간이다.
단어(word)는 일반적으로 띄어쓰기나 줄바꿈과 같은 공백 문자(whitespace)로 나뉘어져 있는 문자열의 일부분이다.
단어를 벡터로 변환하는 경우 단어 임베딩(word embedding)이다. 
각 문장을 벡터로 변환하는 경우 문장 임베딩(sentence embedding)이다. 
단어 임베딩이란 앞서 말씀드린 바와 같이 이 각각 하나의 좌표를 가지도록 형성한 벡터공간이다.
1. Preprocessing : kr-Report_2018.txt 를 읽는다.
2. Tokenization : 문자열(string)을 다차원 벡터(vector)로 변환
3. Token Embedding  (Token 단어) 워드 임베딩 단어가 조각조각 난것이 토큰  [나, 비트, 간다]
4. Document Embedding (Document 문서) s = [ [나 아침 일어났다], [나 비트 간다]] 메트릭스 구조로 바꾼다 

'''


class Solution(Reader):
    def __init__(self):
        self.okt = Okt()
        self.file = File()
        self.file.context = './data/'

    def hook(self):
        def print_menu():
            print('0. Exit')
            print('1. Preprocessing')
            print('2. Tokenization.')
            print('3. Token Embedding')
            print('4. Document Embedding')
            print('5. 2018년 삼성사업계획서를 분석해서 워드클라우드를 작성하시오.')
            print('9. nltk 다운로드')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            elif menu == '1':
                _ = self.preprocessing()
                ic(_)
            elif menu == '2':
                self.tokenization()
            elif menu == '3':
                self.token_embedding()
            elif menu == '4':
                self.document_embedding()
            elif menu == '5':
                self.draw_wordcloud()
            elif menu == '6':
                self.read_stopword()
            elif menu == '7':
                self.remove_stopword()
            elif menu == '8':
                self.read_stopword()
            elif menu == '9':
                Solution.download()

    @staticmethod
    def download():
        nltk.download('punkt')

    def preprocessing(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        file = self.file
        file.fname = 'kr-Report_2018.txt'
        path = self.new_file(file)
        with open(path, 'r', encoding='utf-8') as f:
            texts = f.read()
        texts = texts.replace('\n', ' ')
        tokenizer = re.compile(r'[^ㄱ-힣]+')
        return tokenizer.sub(' ', texts)

    def tokenization(self):
        noun_tokens = []
        tokens = word_tokenize(self.preprocessing())
        # ic(tokens[:100])
        for i in tokens:
            pos = self.okt.pos(i)
            _ = [j[0] for j in pos if j[1] == 'Noun']
            if len(''.join(_)) > 1:
                noun_tokens.append(' '.join(_))
        texts = ' '.join(noun_tokens)
        ic(texts[:100])
        return texts

    def read_stopword(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        file = self.file
        file.fname = 'stopwords.txt'
        path = self.new_file(file)
        with open(path, 'r', encoding='utf-8') as f:
            texts = f.read()
        ic(texts)

        return texts

    def remove_stopword(self):
        tokens = self.tokenization()
        stopwords = self.read_stopword().split(' ')
        texts = [text for text in tokens if text not in stopwords]
        return texts  # 임베딩에 리턴타입은 벡터 임베딩 = 자연어를 벡터로 바꾼것 이미지를 벡터로 바꾼거 음표를 벡터로 바꾼것 소리를 벡터로 바꾼것 임베딩이란것은 내부적으로 리스트
        # 컴프리핸션을 사용한다
        # for i in tokens:
        #     if i not in stopwords:
        #         texts.append(i)
        # print(texts, '\n')

    def token_embedding(self) -> []:
        tokens = self.tokenization()
        stopwords = self.read_stopword()
        texts = [text for text in tokens.split() if text not in stopwords.split()]
        return texts

    # def find_freq(self):
    #

    def draw_wordcloud(self):
        _ = self.token_embedding()
        freqtxt = pd.Series(dict(FreqDist(_))).sort_values(ascending=False)
        ic(freqtxt)
        wcloud = WordCloud('./data/D2Coding.ttf', relative_scaling=0.2,
                           background_color='white').generate(" ".join(_))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def document_embedding(self):
        pass


if __name__ == '__main__':
    Solution().hook()