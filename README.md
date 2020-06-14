# 워드 클라우드 1.0ver

## 설명

Python [한글 정보처리 패키지](https://konlpy-ko.readthedocs.io/ko/v0.4.3) 와 [워드 클라우드 패키지](https://github.com/amueller/word_cloud)를 사용하여 한국어 워드 클라우드 생성 웹페이지를 만들었다. 서버는 장고를 사용했고 배포는 heroku를 이용했다. 

### Python

Django에서 패키지를 이용 한 부분은 API.py로 모듈화했다.

**Code**

```python
# API.py
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

    # 워드 클라우드 이미지 생성하기
    wordcloud = WordCloud(font_path=requsts['word_font'],
                        background_color=requsts['word_background'],
                        colormap=requsts['word_color'],
                        width=requsts['word_width'],
                        height=requsts['word_height']).generate_from_frequencies(dict(tags))
    # 파일 저장
    file_name = '/static/img/' + make_filename() + '.png'
    wordcloud.to_file('./main'+file_name)
    return file_name
```

### Django

Django에서 이미지 처리하는 방법에서 가장 많이 시간을 할애했다. 처음에는 이미지로 처리한 데이터를 데이터베이스에 저장해서 사용하려 했다. 하지만 model에서 처리한 이미지를 저장하는 방법을 찾지 못했다. 그래서 워드 클라우드 패키지에 있는 to_file()을 이용하여 이미지를 저장하고 파일 경로를 반환받는 방법으로 구현했다.

**Code**

```python
# API.py
# 파일 저장
file_name = '/static/img/' + make_filename() + '.png'
wordcloud.to_file('./main'+file_name)
return file_name
```

```html
<!-- result.html -->
<div class="contents well well-lg">
    <div class="page-header">
        <h1>워드 클라우드 <small>이미지를 누르면 저장됩니다</small></h1>
    </div>
    <div class="center_contain">
        <a href="{{ img } }" class="center_contain" download="wordcloud">
            <img src="{{ img } }" alt="결과" class="img_style">
        </a>
    </div>
</div>
```

### Javascript

form을 통해 데이터를 전송하기 전에 데이터의 유효성 검사하는 기능을 javascript로 구현했다.

```html
<!-- main.html -->
<form class="form-horizontal" action="/result" method="POST" onsubmit="return checkForm()">
...
</form>
```

```javascript
// validate.js
const word_width = document.getElementById('word_width');
const word_height = document.getElementById('word_height');
const word_nuber = document.getElementById('word_nuber');
const word_string = document.getElementById('word_string');

// 숫자 유효성 검사
const checknumber = (value) => {
    return !Number.isNaN(value) // 숫자가 맞다면 true
}
// 크기 범위 유효성 검사
const checkrange = (value) =>{
        return (value >= 100 && value <= 1200) ? true : false; // 범위가 맞다면 true
    }
const checkspace = (value) =>{
    const blank_pattern = /^\s+|\s+$/g;
    return value.replace( blank_pattern, '' ) == "" // 공백이면 true
}
//  Form 유효성 검사
const checkForm = () => {
    // 크기에 대한 유효성 검사
    if(checknumber(word_width.value) && checknumber(word_height.value)){
        if(!(checkrange(parseInt(word_width.value)) && checkrange(parseInt(word_height.value)))){
            alert('크기의 범위가 아닙니다');
            return false;
        }
    }else{
        alert('크기의 입력값이 숫자가 아닙니다.');
        return false;
    }
    // 단어수에 대한 유효성 검사
    if(!checknumber(word_nuber.value) || checkspace(word_nuber.value)){
        alert('단어수의 입력값이 숫자가 아닙니다.')
        return false;
    }else if(word_nuber.value > 200 || word_nuber.value < 1){
        alert('단어수의 범위가 아닙니다');
        return false;
    }
    // 내용 공백에 대한 유효성 검사
    if(checkspace(word_string.value)){
        alert('내용의 입력이 공백입니다.')
        return false;
    }
    return true;
}
```

## 한계점

워드 클라우드에서 처리를 마친 데이터를 Django에 저장을 못하는 이슈를 해결하지 못했다. 이로인해 static으로 이미지를 불러와야 했고, 로직상으로는 좋지 않은 방법이라는 것을 알고 있다. 그리고 워드 클라우드를 불러오고 만드는 시간동안 유저에게 보여주는 화면이 지루하다는 점이다. 로딩같은 화면을 보여주면 좋겠지만, Django에서 처리하는 방법을 더 찾아봐야겠다.

다음 버전에는 views.result를 호출하면 기존에 있던 파일을 정리하는 기능을 넣을 것이다. 그리고 마스크 기능과 세부적인 설정을 더 추가할 예정이다.

## 오류

[한글 정보처리 패키지](https://konlpy-ko.readthedocs.io/ko/v0.4.3)은 JDK를 필요로 한다 따라서 그냥 배포를 하면 jvm을 찾지 못한다는 오류가 발생한다. 따라서 Buildpacks에 jvm을 추가해주고 `system.properties` 파일을 생성해주고 `java.runtime.version=1.8`을 추가해준다

```bash
$ heroku buildpacks:set heroku/jvm
```

```system.properties
java.runtime.version=1.8
```