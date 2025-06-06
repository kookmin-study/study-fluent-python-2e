##코드 공부

파이썬 고성능 딕셔너리에는 해시테이블이라는 엔진이 있음.
해시테이블 : 키를 해시함수 숫자로 바꿔서(index화) 그 숫자의 위치값을 저장하는 구조
딕셔너리는 복잡한 해시 테이블 구조가 숨어있기때문에 key구조가 작동하는 것

#3.2

지능형 딕셔너리 : 키-값 쌍을 반복할 수 있는 임의의 반복형 객체를 받아 dict 객체를 생성

ex)
dial_codes = [(100, 'korea'),(101,'japan')]
a = {country: code for code, country in dial_codes}
a = {'korea' : 100, 'japan' : 101}

매핑 언패킹하기는 데이터 사용시 유용하며 딕셔너리 안받는 경우 인수를 전달한다.
함수를 호출할때 키가 모두 문자열이고 전체 인수에서 유일하게 식별할 수 있을때 언패킹 ** 적용 가능

ex)
{'a':0,**{'x':1}} = {'a' :0, 'x' :1}, 나중에나온 값이 먼저 나온 값 덮어씀.

>>그래서 언제 사용하고 유용하긴 한건가?
딕셔너리를 하나하나 꺼내 쓰지 않아도 되게 해서 가독성, 유연성, 재사용성 면에서 유용함.
함수 인자가 많을때 딕셔너리로 정리하고 **로 전달하기.
딕셔너리 내 딕셔너리의 경우 딕셔너리 구조 재구성하거나 api 응답을 다른 함수나 클래스에 맞게 변환할때 딕셔너리를 flatten하게 만들때 사용

| : |을 이용한 매핑 병합
>>연산자 기호 뭐임?

#3.3

match/case문의 대상이 매핑객체일때도 가능

ex)
def get_creators(record: dict) -> list:
    match record:
        case{'type':'book','api':2,'author':[*names]}: #[*names]는 리스트의 모든 요소를 패턴 변수 names에 담아줌
            return names
        case{'type':'book','api':1,'author':name}: #단일값만 담아줌
            return [name]
        case{'type':'book'}:
            raise ValueError #상기 두 조건을 만족하지 못햇으므로 error
        case{'type':'movie','director':name}:
            return [name]
        case _:
            raise ValueError

if문으로 보기 힘든 복잡한 딕셔너리 구조 매칭에 직관적임.

#3.4

해시가능 : 불변성을 만족하여 hash 값을 가질 수 있는 객체
절대 변하지 않고, 다른 객체와 비교할 수 있으면 그 객체를 해시 가능하다고 함.
컨테이너형은 포함된 객체 모두가 불변해야 해시 가능함.

존재하지않는 키로 d[]로 dict 접근하면 error 발생함.
가변값을 갱신하는 방법
dict.get, dict.setdefaulf
>>이런게 있다는 것만 알아두자.

defaultdict를 사용하면 존재하지 않는 키를 검색했을때 default값 반환함.
또는 __missing 메서드를 추가하는 방법도 있음.
>>__missing__메서드 추가하는거 뭔소린지 모르겟음. 파이썬 메서드에 대한 이해 부족, 기본 공부 후 다시 살펴볼 것

#3.6

collections.OrderedDict 클래스 : 개게가 같은지 비교하려고 대응하는 순서를 검사함.
>>3.6 이전 버전의 호환성을 위해 주로 쓰였다지만 굳이 알아야할 필요가 없는듯?

collections.ChainMap 클래스 : 객체 일련의 매핑을 하나의 매핑처럼 검색 가능함.
chainmap 객체는 매핑을 복사하지 않고 참조 보관함. 객체에 값을 추가하거나 갱신하는건 첫번째 매핑에만 영향을 미침.

collections.Counter 클래스 : 각 키에 대한 정수형 카운터가 있는 매핑형임.
키에 대한 갯수를 count해줌.

shelve 모듈 : 문자열 키와 pickle 이진 포맷으로 직렬화된 파이썬 객체 간 매핑을 영구 저장함.
Shelf 객체는 dbm 모듈을 기반으로하는 간단한 키-값 구조의 dbm 데이터베이스임.
>>뭔소리? shelve는 파이썬 객체를 dict처럼 저장하는 고수준 db이고, pickle은 바이너리 저장/복원 모듈, dbm은 문자열 기반 key-value 데이터를 로컬파일로 저장하는 엔진임.

UserDict는 내부에 self.data라는 진짜 딕셔너리를 들고 있고 모든 메서드는 그걸 기준으로 돌아긱때문에 커스터마이징이 가능함.
>>차이가 뭐지..?
dict는 c로 구현된 내장 객체임. userdict는 dict를 흉내내는 클래스일 뿐
userdict은 내부의 self.data에 데이터를 저장하지만, dict는 자기자신에 바로 저장해버림. 커스터마이징하기 힘듬.

#3.7

불변 매핑 : 변경할 수 없는 딕셔너리 객체. 값 읽기 가능, 추가/수정/삭제 불가
mappingproxytype을 써서 보존.
dict를 감싸서 읽기 전용 프록시를 만들어주는 함수임.
딕셔너리는 그대로지만 객체를 통해서 값 조회만 가능하게 함.
proxy : 진짜 대상 객체를 대신해서 중간 또는 행동하거나 감시하는 대리 객체
원본에 직접 접근하지 않고, 프록시를 통해 우회 접근하게 만들고, 기능 제한이나 감시 구조를 바꿔서 제공하는 것
mappingproxytype은 읽기 전용 프록시의 개념

#3.9

키 객체는 반드시 해시 가능해야할 것
키를 통한 접근이 매우 빠름
dict의 베모리 사용량은 많음. 해시 테이블은 항목마다 저장할 데이터가 많기 때문

#3.10

set : 변경 가능한 집합, 해시불가능 > 딕셔너리 키로 사용 불가능
frozen set : 변경 불가능한 집합, 해시가능 > 딕셔너리 키로 사용 가능
>>언제쓰는데?
중복 제거, 집합 연산 시 사용
set의 경우 값이 바뀌어야하는 경우에 사용 가능
frozen set의 경우 딕셔너리 키로 쓰거나 불변이 중요한 경우 사용
집합 리터럴 구문은 수학적 표기법과 동일, 공집합은 반드시 set 표기해야함.


















