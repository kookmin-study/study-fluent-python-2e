import collections
Card = collections.namedtuple('Card',['rank','suit'])

# FrenchDeck class
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
print(repr(deck))
# >>> FrenchDeck(52 cards)
print(deck)
# >>>[Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), ... , Card(rank='A', suit='hearts')]
print(len(deck))
# >>> 52
print(deck[0])
# >>> Card(rank='2', suit='spades')
 
# __len__ 과 __getitem__ 이 없다면?  -> len() 과 []를 처리할 수 없겠지
class FrenchDeck_1:
    def __init__(self,ranks,suits):
        self.ranks = ranks
        self.suits = suits
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]
#    def __len__(self):
#        return len(self._cards)
#    def __getitem__(self, position):
#        return self._cards[position]    

deck_1 = FrenchDeck_1(ranks,suits)
deck_1


# 시퀀스 자료형에서 요소를 무작위로 추출하는 메서드 있음 random.choice()
from random import choice
print(choice(deck))

# deck_1 은 당연히 안되겠지 
#choice(deck_1)
'''
TypeError                                 Traceback (most recent call last)
Cell In[53], line 6
      3 choice(deck)
      5 # deck_1 은 안되겠지
----> 6 choice(deck_1)

File /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/random.py:346,
in Random.choice(self, seq)
    344 """Choose a random element from a non-empty sequence."""
    345 # raises IndexError if seq is empty
--> 346 return seq[self._randbelow(len(seq))]

TypeError: object of type 'FrenchDeck_1' has no len()
'''
# 에러 메시지를 보면, index 에러가 남 -> len(deck_1) 이 안되기 때문이다. 
# 그럼 __len__() 메서드만 추가하면 될까?
# 당연히 안되지 -> 왜냐면, 
# --> 346 return seq[self._randbelow(len(seq))] 여길 보면, 결국 seq(deck_1)을 인덱싱 해야해 -> __getitem__ 메서드를 호출하겠지
# __getitem__() 메서드도 추가 돼야 가능하단 뜻!
'''
__len__() 메서드만 추가해서 실행하면 결국 에러나는 것 확인할 수 있음
--> 346 return seq[self._randbelow(len(seq))]

TypeError: 'FrenchDeck_1' object is not subscriptable
'''
