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
//  Form 유효성 검사
const checkForm = () => {
    // 크기에 대한 유효성 검사
    if(checknumber(word_width.value) && checknumber(word_height.value)){
        if(!(checkrange(parseInt(word_width.value)) && checkrange(parseInt(word_height.value)))){
            alert('크기의 범위가 정확하지 않습니다.');
            return false;
        }
    }else{
        alert('크기의 입력값이 숫자가 아닙니다.');
        return false;
    }
    // 단어수에 대한 유효성 검사
    if(!(checknumber(word_nuber.value))){
        alert('단어수의 입력값이 숫자가 아닙니다.')
        return false;
    }
    // 내용 공백에 대한 유효성 검사
    if(!word_string.value){
        alert('내용의 입력이 공백입니다.')
        return false;
    }
    return true;
}
