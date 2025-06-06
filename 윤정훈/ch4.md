##코드 공부

#4.2

문자의 단위 원소(코드포인트)는 10진수 0에서 1,114,111까지 표현한 숫자
인코딩: 코드 포인트를 바이트 시퀀스로 변환하는 알고리즘

byte와 bytearray의 각 항목은 0에서 255 사이 정수

오로지 str형만 s[0]과 s[:1]이 동일함.
그 외 모든 파이썬 시퀀스는 항목 하나와 길이 1인 슬라이스는 다름.

#4.4

인코딩 방식 종류
1. latin1 : cp1252 등 다른 인코딩 및 유니코드 자체의 기반이 되는 인코딩 방식
2. cp1252 : 기타 기호를 추가한 latin1의 확장방식
3. cp437 : ibm pc에서 사용하던 방식, latin1과 호환되지 않음.
4. gb2312 : 중국 간체자 인코딩 방식
5. utf-8 : 웹에서 8비트 인코딩하는데 가장 널리 쓰이는 방식.
6. utf-16le : 16비트 인코딩 체계

>>업무할때 utf-8-sig, cp949, euc-kr는 써봄 얘네랑의 차이는?
utf-8-sig는 utf-8의 bom을 제거해줌. 엑셀에서 한글깨짐을 방지해줌.
cp949는 euc-kr을 포함한 windows 확, 전통적인 한국어 인코딩 방식임

utf-과 16의 비교
8은 1바이트 단위 16은 2바이트 단위. 이게 어떤 차이?
웹/인터넷은 8 사용, excel/word는 16 사용
utf-8은 영어 기호 숫자가 많을때 효율적, 영어 외 글자당 많은 바이트가 소요될 수록 16이 효율
8은 ascii와 완벽히 호환됨. 
ascii란 정확히 무엇인지? :디지털 세계의 고전 문자 체계
미국표준문자 인코딩

#4.5

인코딩 방식 : 코덱 (coder + decoder)

인코딩/디코딩의 에러
unicodeerror, unicodedecodeerror이 있음.
소스 코드가 예기치 않은 방식으로 인코딩되어 있으면 SyntaxError가 발생하기도 함.

UnicodeEncodeError : str을 byte로 바꿀때 인코딩 방식이 인코딩할 수 없는 문자가 있을 경우
ignore 처리로 넘어갈 수 있으나 좋지 않은 방식 : 문자데이터의 손실을 야기함.
replace 처리는 물음표로 치환하여 어디에 문제가 발생하는지 확인 가능

UnicodeDecodeError : 이진시퀀스를 텍스트로 변환할때 해당 인코딩의 정당한 문자로 변환할 수 없는 경우
해당 에러는 원본을 인코딩 후 다른 코덱으로 디코딩했을때 발생할 가능성이 많음. 또는 기존 인코딩 데이터의 손실이 발생한 경우에도 발생함.

파이썬 3부터는 UTF-8을 소스 코드 기본 인코딩 방식으로 사용.
인코딩을 선언하지 않고 UTF-8 외의 방식으로 인코딩된 모듈을 로딩하면 SyntaxError 발생함.

바이트 시퀀스의 인코딩 방식은 알아낼 수 없다. 반드시 명시되어야 함.

인코딩 추측 방식 있긴 함. > 굳이 당장 알아야할 필요는 없을듯?

BOM : Byte Order Mark
해당 파일이 어떤 인코딩인지 표식 역할을 함.
UTF-16, 32는 바이트 순서가 중요함. 필수임.
UTF-8에서는 선택적이지만 실무에서는 많이 쓰임.
LE(리틀엔디언), BE(빅엔디언)은 순서가 다름.
ex) U+0045에서 리틀엔디언은 45 00 으로 나타나지만 빅엔디언은 00 45 로봄.
BOM이 없다보면 순서를 모르니 문자가 깨질 수 있음.

엔디안이란? : 다중 바이트로 표시되는 숫자들이 메모리에 저장될때 가장 앞에 어떤 바이트를 둘것인지 정하는 방식
역사적 하드웨어 설계에 따른 차이로 혼용되고 있음.

인코딩이 정확히 이해 안돼서 추가 정리
인코딩이란 문자 -> 숫자 -> 바이트 로 변환하는 것
인코딩방식이란 숫자를 어떠한 방식으로 바이트에 저장할지? 에 따라 다름.
모든 문자는 고유번호가 있고 문자의 숫자로의 표현을 유니코드라함.
유니코드를 나타내는 기호가 U+임.
UTF-8은 8진수사용이 아님. 인코딩 자체는 비트로(0과1의 이진수)로 저장하고 우리가 보기 편하게 16진수를 쓰는 것.
ex) 알파벳 A 는 유니코드포인트로 U+0041 10진수로는 65임. 16진수로는 0x41
ASCII는 이걸 01000001 로 저장 <-1바이트
UTF-8도 01000001로 1바이트 저장.
UTF-16은 무조건 2바이트를 사용해야함.[00000000 01000001] 0X00 0X41로 저장
이렇기 때문에 엔디안은 UTF-8에서는 의미없음. 16은 무조건 2바이트 기준이기때문에 순서에 문제발생.

#4.6

텍스트 입출력을 처리할때 가장 훌륭한 방법이 유니코드 샌드위치, 즉 BYTES는 가능한 빨리 STR로 변환해야함.

파이썬 3는 내장함수 OPEN()은 파일을 텍스트 모드로 읽고 쓸때 필요한 모든 인코딩과 디코딩 작업을 수행한다.
위의 문제점은 윈도우의 경우 기본 인코딩을 CP1252로 쓰기때문에 UTF으로 저장 후 인코딩 방식 지정안하고 불러오면 깨짐.

#4.7

유니코드에는 결합문자가 있어 문자열 비교가 간단하지않음.
결합문자란? 기본문자 외 장식으로 붙는문자를 말함. e위에 첨자 있고 그런건듯
이런것들때문에 정규화가 필요함.

NFC 는 가장 짧은 동일 문자열을 생성함.
NFD 는 기본문자와 별도 결합문자를 분리함.
안전을 보장하기 위해 파일 저장 전에 NORMALIZE 를 호출해 문자열을 청소하는 편이 좋음.

NFKC나 NFKD는 호환성을 나타내며 호환문자에 영향을 미침.
즉 의미가 같으면 같다고 보도록 정규화함.

케이스 폴딩: 모든 텍스트를 소문자로 변환하는 작업.
예외가 있기때문에 .lower과는 다른 결과를 반환함.
대소문자 구분없이 문자를 빅할때는 str.casefold가 가장 좋은 방법임.

shave_marks 함수를 써서 발음 구분을 제거하는 방식도 있음.
발음 기호를 제거하면 뜻이 바뀌어 적절한 정규화 형식은 아님.

#4.8

파이썬에서 비아스키 텍스트는 locale.strxfrm()을 이용해서 변환하는 것이 표준
