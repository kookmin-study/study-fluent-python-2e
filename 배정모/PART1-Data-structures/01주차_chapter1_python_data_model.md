# chapter 1 - python data model

## I) 기초 공부
### 1.0.1 컬렉션(Collection)
- 

### 1.0.2 
### 1.0.3
### 1.0.4
### 1.0.5
### sequence, iterator, function, coroutine, class, context-manager
### asdads
- 컬렉션(Collection)
- iterable , iterator 
- interface-class
- 컬렉션
- 구조체
- 추상 클래스, 추상 메서드
- 구상 클래스, 구상 메서드
- sequence, iterator, function, coroutine, class, context-manager

## II) Overview : About pythonic 
- special method(**dunder method**)
    - \_\_len\_\_ / \_\_getitem\_\_ / \_\_repr\_\_ / \_\_str\_\_ / \_\_init\_\_ / \_\_del\_\_ 등
    - 사용자 정의 객체도 dunder method 를 구현하면 파이썬 **내장 객체**처럼 동작할 수 있다.<br>**→ pythonic coding style**
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
        - 이를 통해 내장 객체 처럼 동작할 뿐 아니라, <br>**표준 파이썬 Sequence 객체 처럼 작동**하게 되며, <br>**반복**과 **슬라이싱**은 물론, <br>표준 라이브러리에서 제공하는 random.choice() reversed() sorted() 등도 사용할 수 있다.<br>**→ 파이썬의 시퀀스 프로토콜만 만족하면 기본 기능이 다 됨**<br> **→ Duck Typing 관점의 Sequence**
        <br>**→ (참고) \_\_len\_\_ 의 경우 다음과 같이 동작**
            ```python
            len(self)                         # FrenchDeck의 __len__() 호출
            → self.__len__()                 
            → return len(self._cards)        # 여기서 _cards는 list 객체
            → self._cards.__len__()          # 결국 list의 __len__() 메서드 호출됨
            → 리스트의 길이(int) 반환
            ```
## III)  
## IV) 
