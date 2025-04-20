# chapter 3 Dict And Set - A : Dict
- Contents
    - [About Dict](#1-about-dict)
    - [PyDictObject](#2-pydictobject)
    - [Understanding Mappings from a Duck Typing Perspective](#3-understanding-mappings-from-a-duck-typing-perspective)
    - [Hash Table & Hashable](#4-hash-table--hashable)
    - [Handling for missing keys](#5-handling-for-missing-keys)
    - [About Set](#6-about-set)

## 0. Background
```text
Iterable
├── Collection
│   ├── Sized
│   ├── Container
│   └── Iterable
│
├── Sequence
│   └── str, tuple, range
│
├── MutableSequence
│   └── list, deque, array.array
│
├── Mapping
│   └── MappingProxyType
│
├── MutableMapping
│   └── dict, defaultdict, OrderedDict│
├── Set
│   └── frozenset
│
└── MutableSet
    └── set
```

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| Sequence | 순서 있음, 인덱스 접근 가능, for, in, 슬라이싱 지원 | list, collections.deque, array.array, tuple, str, range |
| **Mapping** | **key - value 구조** | **dict, collections.defaultdict, collections.OrderedDict, collections.chainMap, types.MappingProxyType** |
| **Set** | **순서 없음, 중복 없음, 집합 연산 가능** | **set, frozenset** |


## 1. About Dict
- Dict 
    - Initialize
        ```python
        dict() # new empty dictionary
        dict(mapping) # new dictionary initialized from a "mapping object's (key, value) pairs"
        dict(iterable) # new dictionary initialized as if via:
            """
            d = {}
            for k, v in iterable:
                d[k] = v
            """
        dict(**kwargs) # new dictionary initialized with the "name=value pairs" in the keyword argument list.  For example:  dict(one=1, two=2)
        ```
    - **PyDictObject** 사용(C-level)
    - **Mapping** 구현체(구현클래스) / 서브클래스 / 자료형 
    - 내부구조
        - Open addressing 방식의 Hash Table 자료구조 사용
            - Hashable 객체만 key 로 쓸 수 있는 이유지
        - collision Handling(with Open addressing)
            - linear probing / Quadratic Probing / Double Hashing
        - [more details](#4-hash-table--hashable) 
    - dict[key] / del dict[key] / key in dict 등 : 평균 O(1) , 최악 O(n) -> by collision
    - v3.6 부터 삽입 순서 유지 / v3.7부터 순서 보장

- Dict Comprehension
    ```python
    ex = """I’m going to study hard and become a high-level Python developer""".split(' ')
    myDict = {word : len(word)**2 for word in ex if len(word) > 3 }
    # {'going': 25, 'study': 25, 'hard': 16, 'become': 36, 'high-level': 100, 'Python': 36, 'developer': 81}
    ```
    - 순차적으로 key-value 쌍을 만들어가며, 최종 딕셔너리를 구성하므로, 중간에 이미 존재하는 key인지 판별 불가 -> 덮어쓰기만 가능함

- Dict Unpacking
    ```python
    {**{'a' : 1, 'b' : 2,'c' : 3},'a':77 , 'b':45}
    # {'a': 77, 'b': 45, 'c': 3}
    ```
    - unpacking operator(**)를 사용해 union 가능
    - **중복키 처리** : 위처럼 Dict 리터럴 내에선 가능함. 그게 아닌 인자(매개변수 : **kwargs) 로서 넘길 땐 불가능
        - Error Messege 차이(언어 차원의 문법 처리 vs 런타임 함수 호출 처리)
            ```python
            print(dict(x=1,y=1,x=3))  # SyntaxError: keyword argument repeated: x
            print(dict(x=1,y=1,**{'x':3})) # TypeError: dict() got multiple values for keyword argument 'x'
            ```
            - interpreter 가 parse 단계에서 중복 키워드 인자를 SyntaxError 로 간주 -> 실행 자체가 안됨
            - 문법오류는 없으니, 실행됨 -> 실행시점에 중복 키 인자 충돌발생 -> TypeError

- Dict Union
    ```python
    class MyDict(dict):
        def __or__(self, other):    # __or__ method overloading 필요함. MyDict 로 Wrapping 안하면, 자료형이 dict 따라감
            result = super().__or__(other)
            return MyDict(result)

    dict1 = MyDict(x=1,y=22,**{'z':333,'w':4444})
    dict2 = dict(x=4,y=33,**{'z':222,'w':1111}) # 이게 매개변수로 넘긴거지 -> 여기선 중복키 불가능하다
    merged_dict1 = dict1|dict2
    merged_dict2 = dict2|dict1
    print(merged_dict1, merged_dict2)  # {'x': 4, 'y': 33, 'z': 222, 'w': 1111} {'x': 1, 'y': 22, 'z': 333, 'w': 4444}
    print(type(merged_dict1),type(merged_dict2))    # <class '__main__.MyDict'> <class 'dict'>
    ```
    - 중복 키는 우측 operand / 자료형은 좌측 operand 

- Dict Pattern-matching
    - Pattern-matching 은 PART1 종료 후 따로 정리자료 만들 예정

- [Sample Codes](./codes/03주차_chapter3-1_basic_of_dict.py)

## 2. PyDictObject
- CPython 에서 dict 를 표현하는 구조체 ::  키와 값은 따로 저장됨!!
    ```C
    typedef struct {
        PyObject_HEAD
        PyDictKeysObject *ma_keys;
        PyObject **ma_values;
        Py_ssize_t ma_used;
    } PyDictObject;

    typedef struct {
        Py_ssize_t dk_refcnt;
        Py_ssize_t dk_size;
        char dk_kind;
        ...
        PyDictKeyEntry dk_entries[dk_size]; // 키/값 해시쌍 엔트리 배열
    } PyDictKeysObject;
    ```
    - ma_keys : 실제 키들을 저장하는 테이블(해시 테이블처럼 key/hash(key) 정보 관리)
    - ma_values : value 포인터 배열
    - ma_used : # of key-value pairs

- 같은 키 구조를 공유하는 여러 dict 간 메모리 절약
- 인스턴스 속성 딕셔너리 최적화 (\_\_dict\_\_ 캐시)
- 삽입 흐름 > d = {'x': 1}
    - 'x'의 해시값을 구함
	- ma_keys에서 빈 슬롯을 찾음
	- ma_keys.dk_entries[i].me_key = 'x', 해시 저장
	- ma_values[i] = 1 저장


## 3. Understanding Mappings from a Duck Typing Perspective
- Mapping의 ABC 계층 구조 : Iterable 계열에 속해 있고, 이는 반복 가능한(iterable) 객체라는 뜻
- 따라서 Mapping이 되기 위한 조건은( = 덕 타이핑 관점의 Mapping )
	- 반복 가능(\_\_iter\_\_)
	- 키 기반 접근이 가능 (\_\_getitem\_\_)
	- 크기 (\_\_len\_\_)
    ```python
    from collections.abc import Mapping
    class MyMapping:
        def __getitem__(self, key): 
        def __iter__(self): 
        def __len__(self): 

    isinstance(MyMapping(), Mapping)  # True (덕타이핑 + subclasshook)
    ```
    - Mapping이 내부적으로 \_\_subclasshook\_\_ 메서드를 통해 덕타이핑을 지원하기 때문
- \_\_subclasshook\_\_()
    - isinstance() / issubclass() 호출 시, 해당 클래스를 직접 상속하지 않았어도 서브클래스로 판단해주는 기준(**Duck Typing 판단기준**)
    ```python
    from collections.abc import Mapping

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Mapping:
            if any("__getitem__" not in B.__dict__ or
                "__iter__" not in B.__dict__ or
                "__len__" not in B.__dict__
                for B in C.__mro__):
                return NotImplemented
            return True
        return NotImplemented
    ```

## 4. Hash Table & Hashable
- Hash Table
    - Key - Value 쌍을 저장하는 자료구조
    - Hashing
        - 보통 index 로 바꾸기위해 mod 연산 사용함
        - ex_idx = hash(key) % len(array)
    - 저장
        - 같은 인덱스에 여러 키가 들어올 수 있겠지 -> collision 발생!!
        - **충돌 처리(collision handling)** 필요
    - 검색
        - key -> hash -> index -> array 접근
        - 저장된 key와 ==로 비교해서 값 찾음
    - **충돌 처리(collision handling)**
        - chaining
            ```python
            table = [[] for _ in range(5)]
            def insert(key, value):
                idx = hash(key) % len(table)
                for i, (k, v) in enumerate(table[idx]):
                    if k == key:
                        table[idx][i] = (key, value)  # key 존재하면 갱신
                        return
                table[idx].append((key, value))  # 없으면 추가
            ```
	        - 같은 인덱스에 여러 개 들어오면 리스트로 연결해서 저장
	        - 각 칸이 LinkedList 처럼 됨
            - 구현이 단순하나, realloc시 Locality of Reference 저하로 의한 캐시 효율 저하가 있을 수 있음(heap memory 할당 구조(**선 realloc 후 free**)상 어쩔 수 없음)
            - 참조의 참조구조니까 locality 문제가 심하겠지!
        - **Open Addressing (파이썬 dict는 이거 씀)**
            ```python
            table = [None] * 10
            def insert(key, value):
                idx = hash(key) % len(table)
                while table[idx] is not None:
                    if table[idx][0] == key:
                        break  # 이미 존재하는 키면 덮어쓰기
                    idx = (idx + 1) % len(table)  # linear probing
                table[idx] = (key, value)
            ```
    	    - 빈 자리를 찾을 때까지 배열을 순차적으로 검색해서 저장함
            - 캐시 효율은 상대적으로 좋으나, clustering 문제가 존재함. (아래로 갈 수록 덜함)
	    	- Linear Probing 
                ```python
                index = (index + i) % len(table)
                ```
	    	- Quadratic Probing 
                ```python
                index = (index + i**2) % len(table)
                ```
	    	- Double Hashing (다른 해시 함수 추가 사용)
                ```python
                index = (index + i * hash2(key)) % len(table)
                ```
- Hashable
    - Dict는 Hash Table 자료구조 기반이므로, key 값은 해시가능(hashable)해야함
    - 그렇담 hashable 하단건 뭘까? 
        - **객체 수명주기 동안 불변하는 해시코드**가 있고(\_\_hash\_\_())
        - 다른 객체와 그 값이 **비교가능**(\_\_eq\_\_()) 해야 함
    - **flat immutable type & container immutable type(if all attribute is hashable)**

## 5. Handling for missing keys
- collections.defaultdict
    - default_factory에서 지정한 함수로 기본값을 생성하여 자동으로 추가해줌
    ```python
    from collections import defaultdict

    counter = defaultdict(int)  # default_factory 에 int 생성자를 넘김 -> int() -> 0

    counter['apple'] += 1
    counter['banana'] += 1

    print(counter)  # defaultdict(<class 'int'>, {'apple': 1, 'banana': 1})
    ```
    - list, set, str 등도 default_factory로 지정 가능
    - default_factory는 실제로 키가 존재하지 않을 때만 호출됨
- \_\_missing\_\_()
    - 딕셔너리에서 키 미존재시 행동 정의
    ```python
    class MyMapping(dict) : 
        def __missing__(self, key) :
            if isinstance(key, str) :
                raise KeyError(key)
            return self[str(key)]
        def get(self, key, default = None) : 
            try:
                return self[key]    # dict 의 __getitem__ 에 위임
            except KeyError : 
                return default
        def __contains__(self, key) :
            return key in self.keys() or str(key) in self.keys() 
    ```
    - \_\_missing\_\_은 딕셔너리에서 직접 obj[key] 접근할 때만 동작 -> \_\_getitem\_\_ 실패시 호출되는 거겠지!
    - .get()이나 .setdefault()에는 호출되지 않음 (근데 이게 또 상황에 따라 달라. UseDict의 서브클래스인 경우에 .get 으로 호출되는 경우도 있어)
    - 하여 표준 라이브러리를 상속하여 \_\_missing\_\_ 을 사용하는 경우, 잘 따져봐야한다.

## 6. About Set
- Set
    - 중복 없음 : 같은 값이 여러 번 들어가면 하나로 처리됨
    - 순서 없음 : 인덱스로 접근 불가 (리스트처럼 s[0] 등 불가능)
    - 변경 가능(Mutable) : 값을 추가하거나 제거할 수 있음
    - 내부적으로 **해시 기반**으로 구현됨 : 검색 속도가 빠름 (O(1) 평균)
- Set Literal : {} 
    - 공집합은 set() 함수만 가능함

- Not exists \_\_subclasshook\_\_()
    ```python
    from collections.abc import Set

    class MySet:
        def __contains__(self, item): 
        def __iter__(self): 
        def __len__(self): 

    isinstance(MySet(), Set)  # False : __subclasshook__ 없음
    Set.register(MySet)
    isinstance(MySet(), Set)  # True : 직접등록하면 됨  
    ```
    - Set은 \_\_contains\_\_, \_\_iter\_\_, \_\_len\_\_을 필요로 하나, __subclasshook__이 없기 때문에 덕타이핑 방식의 isinstance() 판별은 안 됨
    - Set을 흉내 내려면 **직접 상속**하거나 **명시적으로 등록**해야 함

- setcomp
    ```python
    squares = {x**2 for x in range(5)}
    print(squares)  # {0, 1, 4, 9, 16}
    ```
    - 중복은 자동 제거됨