# chapter 1 - python data model

## I) Dunder Method : About pythonic 
- special method(**dunder method**)
    - \_\_len\_\_ / \_\_getitem\_\_ / \_\_repr\_\_ / \_\_str\_\_ / \_\_init\_\_ / \_\_del\_\_ 등
    - >사용자 정의 객체도 dunder method 를 구현하면 파이썬 **내장 객체**처럼 동작할 수 있다.<br>🔥`pythonic coding style`
    - **A Pythonic Example**
        ```python
        import collections
        Card = collections.namedtuple('Card',['rank','suit'])
        class FrenchDeck:
            def __init__(self,ranks,suits):
                self.ranks = ranks
                self.suits = suits
                self._cards = [Card(rank, suit) for suit in self.suits
                                                for rank in self.ranks]
                
            def __repr__(self):
                return f"FrenchDeck({len(self)} cards)"

            def __str__(self):
                cards_str = ', '.join(str(card) for card in self._cards)
                return f"[{cards_str}]"
            
            def __len__(self):
                return len(self._cards)

            def __getitem__(self, position):
                return self._cards[position] 

        ranks = [str(n) for n in range(2, 11)] + list('JQKA')
        suits = 'spades diamonds clubs hearts'.split()

        deck = FrenchDeck(ranks,suits)
        print(deck)
        # >>>[Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), ... , Card(rank='A', suit='hearts')]
        print(len(deck))
        # >>> 52
        print(deck[0])
        # >>> Card(rank='2', suit='spades')
        ```
        - dunder method 구현으로 repr() , print()(=\_\_str\_\_ 없으면 \_\_repr\_\_) , len(), [] 연산이 가능. 
        - 심지어 FrenchDeck 클래스는 내부에 self._cards라는 **list**를 두고, 거의 모든 작업을 **위임**하고 있다.
        - >이를 통해 `내장 객체` 처럼 동작할 뿐 아니라, <br>`표준 파이썬 Sequence 객체` 처럼 동작하게 되며, <br>**반복**과 **슬라이싱**은 물론, <br>표준 라이브러리에서 제공하는 random.choice() reversed() sorted() 등도 사용할 수 있다.<br>`파이썬의 시퀀스 프로토콜만 만족하면 기본 기능이 다 됨`<br> `Duck Typing 관점의 Sequence`
        <br>**(참고) \_\_len\_\_ 의 경우 다음과 같이 동작**
            ```python
            len(self)                         # FrenchDeck의 __len__() 호출
            → self.__len__()                 
            → return len(self._cards)        # 여기서 _cards는 list 객체
            → self._cards.__len__()          # 결국 list의 __len__() 메서드 호출됨
            → 리스트의 길이(int) 반환
            ```
        - **" for card in deck: "** 도 가능함 <br>1.iter(deck) 호출됨 > 내부적으로 deck.\_\_iter\_\_ 찾음<br>2.만약 \_\_iter\_\_ 없으면? > \_\_getitem\_\_ 있는지 확인하여, 있으면 index로 돌다가 IndexError 나면 반복 종료
            ```python
            index = 0
            while True:
                try:
                    card = deck[index]
                    # 반복문 안 내용 실행
                    index += 1
                except IndexError:
                    break
            ```
            → 그럼 \_\_iter\_\_가 있을 땐, 어떻게 동작하는기?<br> 
            → \_\_next\_\_ 는 없음 `(list가 iterator는 아님)`<br>
            → 리스트(iterable)의 경우, iter(list) 호출 시, 리스트를 위한 `“리스트 반복자(list_iterator)” 객체`를 만들어줌
        - " card in deck "은 \_\_contains\_\_가 없는데 어떻게 가능한걸까? <br>→ 얘도 비슷함. \_\_getitem\_\_ 을 통해 index 로 돌면서 비교함(Sequence의 경우)<br> → 다 돌면서 비교해야하니 O(n). \_\_contains\_\_ 사용하면, 해시기반의 set 자료형은 O(1)

    >`FrenchDeck은 내부적으로 리스트를 갖고 있고, dunder method를 구현하여 리스트처럼 행동하도록 만든 사용자 정의 클래스 `<br>`🔥 즉, 컨테이너 객체`

## II) 추가 공부
    1.Collection
    2.Interface vs Abstract Class vs Concrete Class
---
### 1.Collection
- 여러 개의 값을 담기 위한 **자료구조**로, 파이썬에서는 여러 개의 데이터들을 한꺼번에 다룰 수 있게 해주는 내장 타입
- 주요 컬렉션 타입 (Built-in Collections)

    | 타입 | 설명 | 예시 | 변경 가능 여부 |
    |------|------|------|----------------|
    | `list` | 순서 있음, 중복 허용 | `[1, 2, 3]` | mutable |
    | `tuple` | 순서 있음, 변경 불가 | `(1, 2, 3)` | immutable |
    | `set` | 순서 없음, 중복 불가 | `{1, 2, 3}` | mutable |
    | `dict` | 키-값 쌍으로 구성된 자료형 | `{"a": 1, "b": 2}` | mutable |
- 컬렉션 공통 특징
    - 대부분 `iterable`  
    - `in` 연산으로 포함 여부 검사 가능  
    - `len()`으로 요소 개수 확인 가능  
    - `for` 루프에서 자주 사용됨
- 참고: 컬렉션 관련 표준 라이브러리
    - `collections.namedtuple`
    - `collections.deque`
    - `collections.defaultdict`
    - `collections.Counter`
    - `collections.OrderedDict`
---
### 2.Interface vs Abstract Class vs Concrete Class
- `2-1.Interface (인터페이스)`
    >**인터페이스**는 구현을 포함하지 않고, 메서드 시그니처만 정의하는 `계약(Contract)`<br> 구현 클래스는 이 인터페이스를 `구현(implements)` 해야함<br>`다중 상속이 가능`
    -  `Java`
        ```java
        interface Flyable {
            void fly();
        }

        interface Swimmable {
            void swim();
        }

        class Duck implements Flyable, Swimmable {
            public void fly() {
                System.out.println("Flying");
            }

            public void swim() {
                System.out.println("Swimming");
            }
        }        
        ```
        - Java 8 이후부터는 `default method 구현`도 가능.<br>→ Java도 파이썬의 `추상 클래스 + 일반 메서드 구조`랑 유사해짐

    - `Python`
        - Python에는 `interface`라는 용어가 없음 
        - ABC (Abstract Base Class)와 `abc` 모듈의 `@abstractmethod`를 활용해 유사하게 구현함
        - 그냥 Interface 가 없고 ABC 로 대체한다 보면됨
        ```python
        from abc import ABC, abstractmethod
        class Flyable(ABC):
            @abstractmethod
            def fly(self):
                pass

        class Swimmable(ABC):
            @abstractmethod
            def swim(self):
                pass

        class Duck(Flyable, Swimmable):
            def fly(self):
                print("Flying")

            def swim(self):
                print("Swimming")
        ```
- `2-2.Abstract Class (추상 클래스)`
    - `일부 메서드만 구현되거나, 전혀 구현되지 않은 클래스로, 직접 인스턴스화할 수 없음`
    - 공통 기능은 구현하고, `구체적 기능은 하위 클래스에서 정의하도록 강제함`
    - **상속을 통해 확장됨** <br> 🔥여기서 문제!! 자바는 추상클래스 다중상속이 안됨!!!
    - `Java`
        ```java
        abstract class Animal {
            abstract void sound();

            void breathe() {
                System.out.println("Breathing");
            }
        }

        class Dog extends Animal {
            void sound() {
                System.out.println("Bark");
            }
        }
        ```
    - `Python`
        ```python
        from abc import ABC, abstractmethod

        class Animal(ABC):
            @abstractmethod
            def sound(self):
                pass

            def breathe(self):
                print("Breathing")

        class Dog(Animal):
            def sound(self):
                print("Bark")
        ```
- `2-3.Concrete Class (구현 클래스)`
    - 모든 메서드가 구현된 클래스
    - 인스턴스화가 가능
    - 상속 없이도 바로 사용 가능

- `2-4.마무리`
    - Java는 **명시적 타입 제약**이 강하며, 인터페이스와 추상 클래스의 개념이 명확히 구분
    - Python은 더 유연함(둘의 구분이 불명확함), `abc` 모듈을 통해 자바 스타일의 추상화 가능
