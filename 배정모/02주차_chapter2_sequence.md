# chapter 2 Sequences - A 
- Contents
    - [Overview of python built-in Sequences](#1-overview-of-python-built-in-sequences)
    - [List comprehension & Generator expression](#2-list-comprehension--generator-expression)
    - [Tuple as a record or immutable list](#3-tuple-as-a-record-or-immutable-list)
    - [Sequence unpacking & pattern matching](#4-sequence-unpacking--pattern-matching)
    - [Slicing](#5-slicing)

## 1. Overview of python built-in Sequences

### Container VS Flat 
- Container Sequence
    - 서로 다른 자료형을 담을 수 있는 시퀀스
    - list / tuple / collections.deque 
    - 객체에 대한 참조를 담는다! -> 개별 요소는 별도 파이썬 객체이다!
- Flat Sequence
    - 하나의 자료형만 담을 수 있는 시퀀스
    - str / bytes / array.array
    - 객체에 대한 참조가 아닌, 그 값을 직접 담는다! (실수 array 가 실수 tuple 보다 메모리 덜 먹는 이유 - **메타데이터 필드**를 안 담으니까!)

### Mutable VS Immutable
- Mutable Sequence
    - 가변 시퀀스 list / bytearray / array.array / collections.deque 
- Immutable Sequence 
    - 불변 시퀀스 tuple / str / bytes 
- 가변시퀀스가 불변시퀀스를 상속하며, 여러 메서드를 추가 구현함
    - Sequence: 읽기 전용 시퀀스를 위한 메서드 정의 (ex. \_\_getitem\_\_, \__\len\_\_)
	- MutableSequence: 여기에 더해 \_\_setitem\_\_, append(), remove() 같은 쓰기/수정 관련 메서드도 요구 
        ```python
        class MutableSequence(Sequence):
            __slots__ = ()

            """All the operations on a read-write sequence.

            Concrete subclasses must provide __new__ or __init__,
            __getitem__, __setitem__, __delitem__, __len__, and insert().

            """

            @abstractmethod
            def __setitem__(self, index, value):
                raise IndexError

            @abstractmethod
            def __delitem__(self, index):
                raise IndexError

            @abstractmethod
            def insert(self, index, value):
        ...
        ```
        - MutableSequence 가 Sequence 를 상속 받음을 확인할 수 있음
        - 추가적인 수정 메서드도 구현되어 있음
        - Full Code 는 `Example Codes` 참고     
- 내장된 구상 시퀀스형이 실제로 Sequence 나 MutableSequence 추상베이스 클래스를 상속받지는 않지만, 이 두 추상 베이스 클래스의 가상 서브클래스이다
    - list, tuple 등이 Sequence 와 MutableSequence를 상속받지 않음
    - abc 모듈에서 register 하여 가상서브클래스화 해 놓음
        ```python
        MutableSequence.register(list)
        MutableSequence.register(bytearray)
        ```
        - Full Code 는 `Example Codes` 참고 
- Example Codes
    - [abc_of_sequence.py](./codes/02주차_chapter2-1_abc_of_sequence.py)

> 🔥 **객체에 대한 참조를 담는다(넘긴다)** 에 대하여... 
>- 🔥 PyObject Structure Of CPython
>   - 파이썬에서 모든 객체는 **C 구조체(PyObject)** 기반
>   - PyObject 기본 구조
>       ```C
>       typedef struct _object {
>           Py_ssize_t ob_refcnt;   
>           PyTypeObject *ob_type;  
>       } PyObject;
>       ```
>       - ob_refcnt: 객체가 몇 번 참조되고 있는지 나타냄 → GC에서 사용됨
>       - ob_type: 이 객체가 무슨 타입인지 가리키는 포인터 (int, list, MyClass 등)
>   - 📌 PyObject는 모든 객체의 공통 기반(Base Struct) 이고, 각 타입별로 여기에 자신만의 구조체가 추가됨
>   - PyFloatObject (float 타입 객체)
>       ```C
>       // 얜 macro 임, 모든 구조체에서 사용될 필드를 미리 정의해두고 복붙해 쓰는 것  
>       #define PyObject_HEAD  \
>       Py_ssize_t ob_refcnt; \
>       PyTypeObject *ob_type;  
>       // PyFloatObject 
>       typedef struct {
>           PyObject_HEAD       
>           double ob_fval;     // float형 실제 값
>       } PyFloatObject;
>       ```
>       - **PyFloatObject는 PyObject를 확장한 구조체**, 실제 float 값은 ob_fval 에 저장됨
>   - 예시!) python에서 a=1.1 (float) 변수를 선언하면...
>       ```C
>       PyObject *
>       PyFloat_FromDouble(double fval)
>       {
>           PyFloatObject *op = _Py_FREELIST_POP(PyFloatObject, floats);
>           if (op == NULL) {
>               op = PyObject_Malloc(sizeof(PyFloatObject));
>               if (!op) {
>                   return PyErr_NoMemory();
>               }
>               _PyObject_Init((PyObject*)op, &PyFloat_Type);
>           }
>           op->ob_fval = fval;
>           return (PyObject *) op;     // PyObject * 타입으로 업캐스팅 해줌 - 모든 객체를 범용적으로 처리하기 위함(Polymorphism)
>       }
>       PyObject *x = PyFloat_FromDouble(1.1);   // PyFloatObject 의 포인터 저장(PyObject * 타입으로)
>       ```
>	    - 힙에 PyFloatObject 구조체 생성됨
>	    - 그 주소를 PyObject*로 업캐스팅해서 반환
>	    - 파이썬 변수 a는 이 포인터를 참조하게 됨
>- 🔥 결론 : 함수 호출 시 “객체 참조를 값으로 전달”한다는 건, 결국 **객체의 주소(포인터)를 복사해 넘기는 것**
>   - "객체 참조"는 C 레벨에서 PyObject* 로 표현되며, 객체 구조체에 대한 **포인터**
>   - 단, 파이썬은 메모리 안전성, 추상화, **가비지 컬렉션(GC)**을 위해
>	    - 메모리 직접 접근 금지
>	    - 포인터 연산 금지
>	    - 객체의 생성/삭제/관리 모두 인터프리터에 위임
>   - 그래서 포인터는 존재하지만, **“접근할 권한은 없음”**
>   - 즉, 파이썬은 포인터를 안전하게 감싼 "참조" 개념만 노출하며, 함수 호출 시 이 포인터가 **값처럼 복사되어** 전달되는 것

> 🔥 Call By Reference? Call By Value? 
>- 🔥 **Call By Object-Reference(Assignment)**
>   - 파이썬의 변수할당은 해당 객체에 대한 binding = 참조를 저장한다(**Pointer같은 주소 개념**)
>       ```python
>       def modify(n):
>           n += 1
>       x = 1.1
>       y=x
>       z=x
>       print(modify(z))    # 2.1
>       print(x)    # 1.1
>       print(z)    # 1.1
>       ```
>       - 1.1은 메모리에 하나의 PyFloatObject로 존재 / x, y, z는 해당 객체의 **주소**를 저장
>       - ob_refcnt = 3 이 되겠지 (이 값이 **GC** 에 활용됨 - 참조 카운팅 기반 메모리 관리)
>       - modify(z) 이 실행되는 순간, 1.1 객체의 참조회수는 4로 잠시 늘어나나(n+=1 연산시 다시 3됨),<br> **immutable 객체이므로,** in-place 가 아닌 **새 객체 생성 + 참조 바꿔치기**
>       - 2.1 은 새로운 PyFloatObject 로 존재하게 되고, n 이 해당 객체 주소를 참조함(함수 종료시엔 사라지겠지 -> GC 대상) 
>       - x, y, z 가 가르키던 1.1 객체는 그대로 존재
>       - 만약 x, y, z 가 리스트 객체를 가르키고, 함수 내에서 리스트 객체 자체를 바꿨다면, 원본에 영향을 줬겠지(mutable 객체 특성)
>- 🔥 결론 : 
>   - 객체 참조(주소)를 넘긴다
>   - 파이썬은, 그 주소 자체를 직접 조작할 수는 없어서 그 주소가 가리키는 객체의 값을 조작할 수 밖에 없다.
>   - 그 객체가 mutable이면 원본 값이 바뀌고,<br>👉 Call by Reference 처럼 보이겠지
>   - 객체가 immutable이면 새로운 객체를 만들어 새 참조로 바꿔치는 것<br>👉 Call by Value 처럼 보이겠지

## 2. List Comprehension & Generator Expression
### List Comprehension(listcomp) 
- sequence 혹은 기타 iterable 객체로부터 새 리스트 객체를 만들기 위함
- **Eager Evaluation**
    ```python
        words = '$#@asdq'
        codes = [ord(word) for word in words]
    ```
- 단, 생성한 리스트를 사용할 것이 아니라면(ex.한 번만 순회하면 될 경우), 안쓰는 것이 좋음
    ```python
        t = tuple([x**2 for x in range(10)])
    ```
    - tuple 을 만들기위해 리스트를 생성할 필요가 없음.(한 번 순회하고 버릴거니까)
    - 리스트가 다 메모리에 올라가는 비효율이 생김
    - genexp 가 효율적(Lazy Evaluation) 

- map()/filter()/lambda expr 조합보다 list comp 가 빠르고 직관적
    - list comprehension은 C로 구현된 내부 루프를 사용하여, 파이썬 인터프리터 레벨의 함수 호출 오버헤드가 없음. (파이썬에선 함수 호출 오버헤드가 큰 비용을 차지함)
    - dis.dis 활용 비교 : 파이썬 인터프리터가 내부적으로 어떤 명령어(opcode)를 실행하는지 알 수 있음
        ```python
        import dis
        dis.dis('[x**2 for x in range(10) if x % 2 == 0]')
        """
        1           0 LOAD_CONST               0 (<code object <listcomp> at 0x1026469d0, file "<dis>", line 1>)
                    2 LOAD_CONST               1 ('<listcomp>')
                    4 MAKE_FUNCTION            0
                    6 LOAD_NAME                0 (range)
                    8 LOAD_CONST               2 (10)
                    10 CALL_FUNCTION            1
                    12 GET_ITER
                    14 CALL_FUNCTION            1
                    16 RETURN_VALUE
        Disassembly of <code object <listcomp> at 0x1026469d0, file "<dis>", line 1>:
        1           0 BUILD_LIST               0
                    2 LOAD_FAST                0 (.0)
                >>    4 FOR_ITER                24 (to 30)
                    6 STORE_FAST               1 (x)
                    8 LOAD_FAST                1 (x)
                    10 LOAD_CONST               0 (2)
                    12 BINARY_MODULO
                    14 LOAD_CONST               1 (0)
                    16 COMPARE_OP               2 (==)
                    18 POP_JUMP_IF_FALSE        4
                    20 LOAD_FAST                1 (x)
                    22 LOAD_CONST               0 (2)
                    24 BINARY_POWER
                    26 LIST_APPEND              2
                    28 JUMP_ABSOLUTE            4
                >>   30 RETURN_VALUE
        """ 
        ```
        - FOR_ITER, BINARY_MODULO, COMPARE_OP, BINARY_POWER 와 같은 간단한 연산 opcode 위주
	    - 함수 호출 없이 루프를 직접 순회함 → 빠름! 
        ```python
        dis.dis('list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(10))))')
        """
        1           0 LOAD_NAME                0 (list)
                    2 LOAD_NAME                1 (map)
                    4 LOAD_CONST               0 (<code object <lambda> at 0x104a4ea80, file "<dis>", line 1>)
                    6 LOAD_CONST               1 ('<lambda>')
                    8 MAKE_FUNCTION            0
                    10 LOAD_NAME                2 (filter)
                    12 LOAD_CONST               2 (<code object <lambda> at 0x104a4eb30, file "<dis>", line 1>)
                    14 LOAD_CONST               1 ('<lambda>')
                    16 MAKE_FUNCTION            0
                    18 LOAD_NAME                3 (range)
                    20 LOAD_CONST               3 (10)
                    22 CALL_FUNCTION            1
                    24 CALL_FUNCTION            2
                    26 CALL_FUNCTION            2
                    28 CALL_FUNCTION            1
                    30 RETURN_VALUE

        Disassembly of <code object <lambda> at 0x104a4ea80, file "<dis>", line 1>:
        1           0 LOAD_FAST                0 (x)
                    2 LOAD_CONST               1 (2)
                    4 BINARY_POWER
                    6 RETURN_VALUE

        Disassembly of <code object <lambda> at 0x104a4eb30, file "<dis>", line 1>:
        1           0 LOAD_FAST                0 (x)
                    2 LOAD_CONST               1 (2)
                    4 BINARY_MODULO
                    6 LOAD_CONST               2 (0)
                    8 COMPARE_OP               2 (==)
                    10 RETURN_VALUE
        """
        ```
        - MAKE_FUNCTION, CALL_FUNCTION이 반복 실행(lambda 함수 계속 호출) → 함수 호출 오버헤드 증가
	    - range(10) → filter → map → list() 순으로 중첩 호출
    - 속도 비교 예시
        - [check_speed_of_listcomp.py](./codes/02주차_chapter2-2_check_speed_of_listcomp.py)

### Generator Expression(genexp)
- 생성자에 전달할 데이터를 통째로 만들지 않고, iterator protocol을 이용하여, 필요할때 하나씩 생성함.
- **Lazy Evaluation**
    ```python
    squares = (x**2 for x in range(10))
    print(squares)  # <generator object <genexpr> at 0x100523510>
    print(next(squares))    # 0
    print(next(squares))    # 1
    print(next(squares))    # 4
    print(next(squares))    # 9
    ```
- example of **Cartesian Product**
    ```python
    colors = ['black','green','yellow']
    sizes = ['S','M','L','XL']
    for cloth in (f"{c}_{s}" for c in colors for s in sizes):
        print(cloth)
    """output
    black_S
    black_M
    black_L
    black_XL
    green_S
    green_M
    green_L
    green_XL
    yellow_S
    yellow_M
    yellow_L
    yellow_XL
    """
    ```


## 3. Tuple as a record or immutable list
- As a Record
    ```python
    traveler_ids = [('USA','1234123'),('BRA','8174816'),('KOR','1898519490'),('ESP','98171535748')]
    for passport in traveler_ids :
        print('%s/%s' % passport)
    
    for country, _ in traveler_ids :
        print(country)
    ```
    - for 루프 돌 때, passport 변수가 리스트 내 각 튜플객체에 binding
    - for 루프는 튜플의 각 요소를 가져오는 방법을 앎 -> **Unpacking**
    - 관심 없는 요소는 더미변수를 나타내는 _ 주로 사용함 
        - 위의 경우 언더바도 binding 됨.  match/case 문 에선 binding 안 됨.

- As a Immutable List
    - list 보다 메모리를 적게 소비하는 tuple 
        - 길이가 고정되어 있으니 필요한 만큼만 메모리 할당. list 는 추가할 것 생각해 좀 더 할당함.
        - tuple 요소에 대한 참조는 tuple 구조체에 배열로 저장됨. list 는 다른 곳에 저장된 참조 배열에 대한 포인터를 가짐 <br>-> 요소가 늘어나면, 공간을 새로 확보하고 참조 배열 재할당 필요하므로<br>-> CPU Cache 효율 감소


## 4. Sequence unpacking & pattern-matching
- Sequence Unpacking
    - 기본 unpacking
    ```python
    import os
    path = '/Users/jeongmo/local-git-repo/study-fluent-python-2e/배정모/sync-with-upstream.sh'
    _, filename = os.path.split(path)   # (path, last_part) tuple 생성 & unpacking
    print(filename) # sync-with-upstream.sh
    ```
    - 확장 unpacking
    ```python
    a, *b = [1, 2, 3, 4]
    print(a, b)  # 1, [2, 3, 4]
    a, *b, c = [1, 2, 3, 4, 5]
    print(a, b, c)  # 1 [2, 3, 4] 5
    ```
    - enumerate, zip 같은 iterable 객체도 전부 unpacking 가능하다
    ```python
    la = ['A', 'B', 'C']
    lb = [1, 2, 3]
    lc = [9, 8, 7]
    for a, b, c in zip(la, lb, lc):
        print(a, b, c)
    ```
- Sequence Pattern Matching(py 3.10~)
    ```python
    def test(seq):
    match seq:
        case [1, 2, 3]:
            return "정확히 [1, 2, 3]과 일치!"
        case [1, 2, _]:
            return "세 번째 값은 무시하고 [1, 2, _] 패턴과 일치!"
        case [1, *rest]:
            return f"1로 시작하고 나머지는 {rest}!"
        case _:
            return "어떤 패턴에도 안 맞음"
    ```
    - 언패킹 + 와일드카드 조합
    ```python
    def test(seq):
    match seq:
        case [_, second, *_]:
            return f"두 번째 값은 {second}"
    ```
## 5. Slicing    
- 슬라이스 객체 : slice(start, stop, step) - 서브리스트를 만들기 위한 인덱스 정보(start, stop, step)를 담고 있는 객체
- 동작 방식 
    ```python
    lst[1:4]
    # slice(1, 4)
    # print(s.start, s.stop, s.step)  -> 1 4 None
    ```
    - slice(1, 4) 객체생성
	- lst.\_\_getitem\_\_(slice(1, 4)) 호출
    - **즉, 슬라이싱은 실제로는 인덱스 접근이 아니라 slice 객체를 인자로 넘기는 함수 호출!**
- 파이썬 리스트는 슬라이스 할당 시 iterable만 허용하도록 구현되어 있음 
    ```python
    l = list(range(10)) # [0,1,2,3,4,5,6,7,8,9]
    l[2:5] = [100] # [0,1,100,5,6,7,8,9]
    l[2:5] = 100 # TypeError : can only assign iterable
    ```
    - 왜그럴까? : slicing 은 결국 slice 객체를 \_\_getitem\_\_ 메서드 \_\_setitem\_\_ 메서드 인자로 넘기는것.. 아래를 보면 왜 iterable 이어야 하는지 이해가 갈것임...
    - iterable 이 아닌 그냥 값으로 쓰고싶다면, indexing 을 해야겠지... 
- \_\_getitem\_\_ , \_\_setitem\_\_ 직접 구현해보자(왜 iterable 객체만 할당가능한지 알게될거야)
    ```python
    class MyList:
        def __init__(self,data):
            self.data = data # [10, 20, 30, 40, 50] 리스트 받는다 가정. 단, 구현은 직접
    
        def __getitem__(self, index):
            if isinstance(index, slice):
                indices = range(*index.indices(len(self.data)))
                return [self.data[i] for i in indices]   #이런 방식으로 도는거
            elif isinstance(index, int):
                return self.data[index]
            else:
                raise TypeError
    
        def __setitem__(self, index, value):
            if isinstance(index, slice):
                indices = list(range(*index.indices(len(self.data))))
                for i in reversed(indices):
                    del self.data[i]
                insert_at = indices[0] if indices else len(self.data)
                for offset, v in enumerate(value):     # 왜 slice 객체를 통한 할당이 iterable 객체만 가능한지 알 수 있지
                    self.data.insert(insert_at + offset, v)
            elif isinstance(index, int):
                self.data[index] = value
            else:
                raise TypeError
    ```


