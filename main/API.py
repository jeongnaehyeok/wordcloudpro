from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import random
import string

# 파일 이름 만들기(return 파일이름)
# 렌덤값으로 만들기
def make_filename():
    char_set = string.ascii_lowercase + string.digits
    file_name = ''.join(random.sample(char_set*6, 6))
    return file_name

# 워드 클라우드 생성 함수(return 경로)
def wordcloud_maker(requsts):
    # 한글 형태소 분석하기
    engin = Okt()
    nouns = engin.nouns(requsts['word_string'])
    nouns = [n for n in nouns if len(n) > 1]

    # 단어 숫자 세기
    count = Counter(nouns)
    tags = count.most_common(requsts['word_nuber'])

    # 워드클라우드 이미지 생성하기
    wordcloud = WordCloud(font_path=requsts['word_font'],
                        background_color=requsts['word_background'],
                        colormap=requsts['word_color'],
                        width=requsts['word_width'],
                        height=requsts['word_height']).generate_from_frequencies(dict(tags))
                        
    # 파일 저장
    file_name = '/static/img/' + make_filename() + '.png'
    wordcloud.to_file('./main'+file_name)
    return file_name
