# chapter 1 - python data model

## I) Dunder Method : About pythonic 
- special method(**dunder method**)
    - \_\_len\_\_ / \_\_getitem\_\_ / \_\_repr\_\_ / \_\_str\_\_ / \_\_init\_\_ / \_\_del\_\_ 등
    - 사용자 정의 객체도 dunder method 를 구현하면 파이썬 **내장 객체**처럼 동작할 수 있다.<br><span style="color:red">**→ pythonic coding style**</span>
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
        - 이를 통해 내장 객체 처럼 동작할 뿐 아니라, <br><span style="color:red">**표준 파이썬 Sequence 객체 처럼 동작**</span>하게 되며, <br>**반복**과 **슬라이싱**은 물론, <br>표준 라이브러리에서 제공하는 random.choice() reversed() sorted() 등도 사용할 수 있다.<br>**→ 파이썬의 시퀀스 프로토콜만 만족하면 기본 기능이 다 됨**<br> **→ Duck Typing 관점의 Sequence**
        <br>**→ (참고) \_\_len\_\_ 의 경우 다음과 같이 동작**
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
            → \_\_next\_\_ 는 없음 (list가 iterator는 아님)<br>
            → 리스트(iterable)의 경우, iter(list) 호출 시, 리스트를 위한 “리스트 반복자(list_iterator)” 객체를 만들어줌
        - " card in deck "은 \_\_contains\_\_가 없는데 어떻게 가능한걸까? <br>→ 얘도 비슷함. \_\_getitem\_\_ 을 통해 index 로 돌면서 비교함(Sequence의 경우)<br> → 대신 다 돌면서 비교해야하니 O(n)이지. 해시기반의 set 자료형이면 O(1) 이겠지

        - FrenchDeck은 <span style="color:red">**내부적으로 리스트를 갖고 있고**, dunder method를 구현하여 리스트처럼 행동하도록 만든 사용자 정의 클래스 <br>→ 즉, **컨테이너 객체**</span>

## II) 추가 공부
- 컬렉션(Collection)
- 구조체
- Interface vs Abstract-Base-Class(ABC) vs 구상클래스
    - java
    ```java java
    public void main
    ```
    - python