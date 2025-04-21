# 딕셔너리와 집합

## 일반적인 맵핑형
- 파이썬 맵핑형은 collection.abc에서 Mapping 및 MutableMapping 추상 베이스 클래스(ABC) 제공
- 추상 베이스 클래스는 매핑에 제공해야하는 최소한의 인터페이스를 정의 및 문서화 / isinstance() 테스트 기준
- 표준 라이브러리에서 제공하는 매핑형은 모두 dict을 사용 -> key가 hash 가능해야함

<details>
<summary>해시 가능이란?</summary>

- 결코 변하지 않는 해시값을 가지고 있고(__hash__메서드)
- 다른 객체와 비교 가능(__eq__메서드)
- 동일한 객체는 반드시 해시값 동일
- 원자적 불변형(str, byte, 수치형) 모두 해시 가능
- frozenset 해시 가능
- 튜플은 내부 항목이 모두 해시 가능해야 가능
- 사용자 정의 자료형은 해시가능
    - 사용자 정의 자료형은 __eq__()나 __hash__()를 오버라이드하지 않으면 기본적으로 해시 가능하다.
    - 이유는 object의 __hash__()가 id 기반으로 정의되어 있기 때문.
    - 그러나 __eq__()만 정의하고 __hash__()는 생략하면, 해시 불가능한 객체가 된다 (set/dict에 못 씀).
    - id(obj) : 객체의 고유한 식별자 반환
        - 객체가 살아있는 동안 유일한 정수값(메모리 주소와 같거나 유사)
        - C포인터 주소값 그대로 리턴 
</details>

## Dictionary
- 지능형 딕셔너리
  - 리스트처럼 가독성 좋게 개발하기 좋음
  - dic = {key:value for key, value in values}
- unpacking
  - 함수 인자로 *는 위치 인자로 튜플 받음 / **는 키워드 인자로 딕셔너리 받음
  - ** 키워드 여러번 사용 가능
- | 연산자
  - 맵핑 병합용
  - 아직 써본적은 없다...
- Key not found 에러를 피하려면...
  -  get() 메서드 활용
     -  키가 없으면 None 또는 기본값
  -  setdefault()
     -  키가 없으면 기본값으로 추가, 있으면 아무것도 안함
     -  리스트나 집합 같은 가변타입 추가 시 많이 활용
  -  defaultdict(from collections)
     -  ```python
            from collections import defaultdict
            fruits = defaultdict(int)
            fruits["apple"] += 1  # 키 없어도 0으로 시작해서 +1 됨
            group = defaultdict(list)
            group["students"].append("jay")  # 자동으로 빈 리스트 생성 ```

- __missing(key)
  - dictionary에 없는 키에 접근 시 자동 호출
  - dict를 상속해서 커스터마이징 시 유용
  - defaultdict도 내부적으로는 __missing__ 매서드 활용

- collections.ChainMap
  - 여러 개의 딕셔너리를 묶어서 하나처럼 보이게 해줌
  - 키를 찾을 때 앞쪽부터 차례로 찾고, 없으면 다음에서 찾음
  - 스코프 체인처럼 작동(파이썬 변수 찾기)
  - 기본 설정값 vs 사용자 설정을 병합하고 싶을 때 활용
  - 여러 환경(예: local, dev, prod 등)의 config를 겹치지 않게 조합하고 싶을 때
  - ChainMap 자체는 값을 "합쳐 보여주기만" 함 → 원본 딕셔너리는 그대로 있음
  - 수정은 항상 첫 번째 딕셔너리에만 반영됨

- shelve.Shelf
  - 파일에 저장되는 딕셔너리
  - 내부적으로는 pickle 사용해서 직렬화 후 파일에 저장
  - key는 문자열 / value는 Python 객체
  - 파일로 만들어서 나중에 객체 그대로 활용 가능

- immutable mapping 방법
  - MappingProxyType 활용
  - read만 가능하도록 하고 변경은 불가하도록 wrapping 된 객체만 보여줌

## Set
- 집합은 고유한 객체의 모음
- 중복 항목이 존재하지 않음(Hashable)
- 지능형 집합으로 집합 정의 가능
- 집합에 속하는 지 검사하는 연산이 매우 효율적이라 집합 연산이 많이 활용 될 것 같을 때 자료형으로 활용
- 다만 메모리 사용이 크다
  - 포인터 배열과 같은 저수준 자료구조와 비교 시
  - set은 해시 기반의 동적 해시 테이블 구조
  - 내부적으로 빈 슬롯 + 포인터 + 오버헤드가 많음
  - 저수준 포인터 배열
    - 고정된 크기
    - 메모리 연속적 할당
    - 오버헤드 거의 없음
    - 요소 직접 접근
  - 집합
    - 요소들을 해시값으로 빠르게 찾기 위한 구조
    - 중복 방지를 위해 해시 충돌 관리 구조 필요
    - 내부에 비어있는 버킷 많음
    - set에 요소 10개만 넣어도 슬롯이 32, 64개씩 생김(성능 위해 미리 공간 확보)
    - 각 요소는 포인터 + PyObject 구조체 + 해시값 등
  - 집합 연산자 매우 다양 -> 코테에 활용하기 좋을듯?
  - dict 뷰(keys(), items()) 또한 집합과 호환 가능
<details>
<summary>PyObject 구조체란?</summary>

-  C언어로 구현된 파이썬 객체의 기본 구조체
-  모든 파이썬 객체는 이 PyObject 구조체를 기반으로 만들어짐
-  ```C
        typedef struct _object {
            Py_ssize_t ob_refcnt;     // 레퍼런스 카운트 (참조 수)
            struct _typeobject *ob_type;  // 객체의 타입 정보 (예: int, list 등)
        } PyObject;
    ```
- 이걸 기반으로 해서 PyLongObject, PyListObject 등 다양한 타입이 확장 구조체로 만들어짐!
- 이 구조 때문에 is 연산자나 id() 같은 게 메모리 주소 기반으로 작동 가능함
- ob_type 덕분에 파이썬은 동적 타입 언어지만 내부적으로 정확히 어떤 타입인지 추적 가능
- ob_refcnt 덕분에 레퍼런스 카운트 기반 가비지 컬렉션이 가능
</details>