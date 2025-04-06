# chapter 2 - Sequences
- Contents
    - [Overview of python built-in Sequences](#1-overview-of-python-built-in-sequences)
    - [List comprehension & Generator expression](#2-list-comprehension--generator-expression)
    - [Tuple as a record or immutable list](#3-tuple-as-a-record-or-immutable-list)
    - [Sequence unpacking & pattern matching](#4-sequence-unpacking--pattern-matching)
    - [Slicing](#5-slicing)
    - [Other Sequences(array, deque etc)](#6-other-sequencesarray-deque-etc)

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
        - 추가적으로 추가적인 수정 메서드도 구현되어 있음
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

> 🔥 왜 python은 Call By Reference 처럼 보이기도하고 Call By Value 처럼 보이기도 할까? 에 대하여...
>- 🔥 **Call By Object-Reference(Assignment)**
>   - 파이썬의 변수할당은 참조를 저장한다(**Pointer**)
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
>- 🔥 결론 : python은 객체 참조를 전달하므로,<br>mutable 객체라면 값을 in-place 하므로 Call by Reference 같이,<br> immutable 객체라면 새로운 객체를 만들어 참조를 바꿔주는 방식으로 동작하므로 Call by Value 같이 보이는 것 
>   - 참조(주소)를 넘긴다
>   - 파이썬은, 그 주소 자체를 직접 조작할 수는 없어서 그 주소가 가리키는 객체의 값을 조작할 수 밖에 없다.
>   - 그 객체가 mutable이면 원본 값이 바뀌고,<br>👉 Call by Reference 처럼 보이겠지
>   - 객체가 immutable이면 새로운 객체를 만들어 새 참조로 바꿔치는 것<br>👉 Call by Value 처럼 보이겠지

## 2. List comprehension & Generator expression
### listcomp 
### genexp

## 3. Tuple as a record or immutable list
## 4. Sequence unpacking & pattern-matching
## 5. Slicing    
## 6. Other Sequences(array, deque etc)    