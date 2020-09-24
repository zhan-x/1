import jieba #结巴分词
import gensim #自然语言处理库 
import re #正则表达式库
import collections #词频统计库
from collections import defaultdict

 #读取文本文件路径，获取文本内容
def read(path):
    content = ''
    file = open(path, 'r', encoding='UTF-8') #只读
    line = file.readline()
    while line:
        content += line
        line = file.readline()
    file.close()
    return content
 
 #过滤标点符号等特殊符号，进行jieba分词，同时将低频词汇去掉
def text_filter(content):
    newtext = []
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")   #定义正则表达式匹配模式
    content = pattern.sub("",content)  # 只保留英文a-zA-z、数字0-9和中文\u4e00-\u9fa5的结果。
    newtext = jieba.lcut(content)  #分词
    documents=[content]#将存储文档到列表
    texts=[[word for word in document.split()]
    for document in documents]
    #计算出词语的频率
    frequency=defaultdict(int)#构建频率对象
    for text in texts:
         for token in text:
             frequency[token]+=1
             texts=[[word for word in text if frequency[token]>50]#如果词汇量过多，去掉低频词
             for text in texts]
             return newtext


 #利用余弦公式计算文本相似度
def cos_similarity(text1,text2):
    texts=[text1,text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts] #只保留英文a-zA-z、数字0-9和中文\u4e00-\u9fa5的结果。
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
   
 
if __name__ == '__main__':
    path1 = r'C:\Users\98577\Desktop\test\orig.txt'  #论文原文的文件的绝对路径
    path2 = r'C:\Users\98577\Desktop\test\orig_0.8_add.txt'  #抄袭版论文的文件的绝对路径
    save_path = r'C:\Users\98577\Desktop\test\output.txt'   #输出结果绝对路径
    content1 = read(path1)
    content2 = read(path2)
    text1 = text_filter(content1)
    text2 = text_filter(content2)
    cos_result = cos_similarity(text1, text2)
    print("文章相似度： %.4f"%cos_result)
    #将相似度结果填入指定文件中
    file = open(save_path, 'w', encoding="utf-8") #只写
    file.write("文章相似度： %.4f"%cos_result)
    file.close()