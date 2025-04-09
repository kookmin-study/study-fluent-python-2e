# chapter 2 Sequences - B
- Contents
    - [Tuple as a record or immutable list](#3-tuple-as-a-record-or-immutable-list)
    - [Sequence unpacking & pattern matching](#4-sequence-unpacking--pattern-matching)
    - [Slicing](#5-slicing)
    - [Other Sequences(array, deque etc)](#6-other-sequencesarray-deque-etc)

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
    ```python
    
    ```
- Sequence Pattern Matching(py 3.10~)
    ```python
    
    ```
## 5. Slicing    

## 6. Other Sequences(array, deque etc)   


