##코드 공부

#5.2

데이터클래스란?
파이썬의 일반적인 클래스와는 기능적으로 동일
주로 데이터를 저장하기위한 용도로 설계된 데코레이터가 적용된 클래스
init repr eq는 기본적으로 제공은 되어있으나 클래스내 사용시 직접 정의해줘야함.
데이터클래스는 얘네가 정의된 상태로 바로 사용 가능함.
dataclass는 클래스가 아니고 클래스를 받아서 바궈주는 함수임.

결국 데이터클래스는 일반 클래스를 dataclass라는 함수를 통해 init repr eq등의 메소드 등을 정의한채로 뱉어낸 클래스 객체인 것

>>collections.namedtuple, typing.NamedTuple 얘네는 왜씀?
dataclass는 기본적으로 가변 데이터
namedtuple이나 NamedTuple은 불변 데이터
불변성이 중요한 코드에서는 더 안전함
namedtuple은 튜플을 상속받기때문에 가벼움
namedtuple collection 내 메소드로 이름표를 붙인 튜플(가볍고 빠름)
NamedTuple typing 내 메소드로 타입 검사까지 되는 튜플클래스

dataclass 데코레이터는 키워드 인수를 받음. (frozen, order, slot) 등

#5.3

>>명명된 튜플을 하면 좋은점?
튜플의 가벼움을 가져가면서 클래스처럼 의미있는 이름으로 접근 가능

#5.4

typing.NamedTuple과 collection.namedtuple의 차이는 annotations__클래스 속성 뿐임.
어노테이션 클래스란 타입힌트를 붙인 클래스.
즉 자료형 힌트는 함수 인수, 반환값, 변수, 속성으로 받을 값을 선언하는 방법임.

#5.6

@dataclass가 받는 키워드 매개변수
1. init __init__ 생성
2. repr __repr__ 생성
3. eq __eq__ 생성
4. order __lt__, __le__, __gt__, __ge__ 생성
5. unsafe_hash __hash__생성
6. frozen 인스턴스를 불변형으로 만듬.

>>frozen이 있으면 굳이 명명튜플을 쓸 이유가?
frozen을 하더라도 여전히 느리고 무거움. 명명해야 구조화되어있기때문에 지정도 편리함.

@dataclass 데코레이터에서
가변 객체를 사용시 모든 인스턴스가 같은 리스트를 공유하기때문에 버그가 날 가능성이 높음.
default_factory를 사용하여 인스턴스마다 새로운 리스트를 사용함.
리스트뿐만아니라 가변객체 모두 문제 (dic, bytearray, set 등)

field()함수는 @dataclass 내에서 각 필드의 설정을 커스터마이즈할 수 있는 함수.
1. default 필드의 기본값
2. default_factory 기본값을 생성하는 무인수 함수
3. init init 필드를 매개변수에 포함
4. repr 필드를 repr이 출력하게 함
5. compare 필드를 eq lt 등의 비교 메서드를 사용하게 함
6. hash 필드를 hash계산에 포함
7. metedata 사용자 정의 데이터의 매핑

>> 5.6 이후 챕터들 뭔소리인지 모르겠음.. 클래스 객체에 대한 이해 더 필요

>> 5.8도 이해 안감. 뭔소리?


