# 프로젝트 과제: LottoBox – 나만의 로또 기록 저장소 만들기

## 목적
파이썬의 핵심 개념(데이터 모델, 시퀀스/매핑, 유니코드 처리, 데이터 클래스, 메모리 관리 등)을 실제 프로젝트에 통합하여 학습 내용을 정리하고, 실용적인 프로그램을 완성해본다.

---

## LottoBox 요구사항

### 0. 로또 한 건의 정보를 깔끔하게 정의하고 싶다.
예: 회차, 구매 번호, 당첨 번호, 몇 개 맞았는지, 등수, 등록 시간 등  
→ `@dataclass`를 사용하여 `LottoRecord` 클래스로 정의하면 자동으로 비교, 출력, 정렬 등이 편리해진다.

---

### 1. 로또 구매 이력을 확인할 수 있어야 한다.
예: `box[0]` 또는 `box[-1]`처럼 사용하고 싶다.  
→ `__getitem__` 메서드 정의 필요

---

### 2. 특정 회차의 기록이 존재하는지 알고 싶다.
예: “1103회차는 이미 등록되어 있나?”  
→ `__contains__`, 또는 `is_duplicate(round: int)` 정의 필요

---

### 3. 특정 회차에 어떤 번호를 구매했는지 알고 싶다.
예: “1102회차에는 내가 어떤 번호를 샀더라?”  
→ `get_my_numbers(round: int)` 같은 헬퍼 메서드 필요

---

### 4. 새로운 구매 기록을 추가할 수 있어야 한다.
예: `box.append(record)`  
→ `append`, `insert`, `__setitem__`, `__len__` 등 시퀀스 메서드 구현 필요  

➕ 추가 조건: 회차별로 최초 구매 시에는 `winning_numbers`를 직접 입력하지 않고, **다음 회차 구매 이력이 입력되는 순간 자동으로 난수 추첨**이 진행되어 당첨 번호가 생성되며, 동시에 등수도 계산되어야 한다.<br>
→ 또한 **가장 최근에 등록된 회차만 추가 구매가 가능**하다. 예: 최근 회차가 1103이면, 1102 같은 지난 회차는 "이미 지난 회차입니다"라는 메시지와 함께 구매 불가 처리해야 함.

---

### 5. 이미 등록된 회차에 다시 추가 구매를 시도했을 때, 그 사실을 알려줘야 한다.
예: “1102회차는 이미 등록되어 있습니다. 추가로 구매하시겠습니까?”  
→ 기존 기록을 보여주고, 추가 여부를 확인하는 흐름이 필요함  
→ 중복 탐지를 위해 `__eq__`, `__hash__`, 내부에 `set` 또는 `dict`로 관리

---

### 6. 당첨 번호를 바탕으로 내가 몇 등인지 자동 판별되길 원한다.
예: 6개 맞췄으면 “1등”, 4개면 “4등”  
→ `check_rank(record: LottoRecord) -> str` 메서드 필요

---

### 7. 모든 기록을 다른 프로그램이나 저장소로 옮기기 쉽게 표현할 수 있어야 한다.
예: 기록을 텍스트가 아닌 컴퓨터가 읽을 수 있는 형태(바이트)로 만들어서 API나 파일에 저장하고 싶다.  
→ `export_bytes()` 메서드 필요 (`str.encode('utf-8')` 활용)

---

### 8. 가장 최근에 봤던 회차 기록을 빠르게 다시 불러오고 싶다.
예: 자주 보는 회차는 캐시해서 빠르게 접근하고 싶음  
→ `weakref` 기반 캐시 기능 구현 가능

---

## 학습 포인트 매핑
| 챕터 | 학습 개념 | 적용 기능 예시 |
|--------|------------|--------------------|
| CH1 | 데이터 모델 | `__getitem__`, `__repr__`, `__eq__`, `__hash__` |
| CH2 | 시퀀스 프로토콜 | `MutableSequence` 상속, 슬라이싱, 정렬 등 |
| CH3 | dict/set 활용 | 회차별 중복 관리, 빠른 조회 |
| CH4 | 유니코드/바이트 | UTF-8 인코딩, `export_bytes()` 구현 |
| CH5 | 데이터 클래스 | `@dataclass`, `frozen=True`, `default_factory` |
| CH6 | 참조 추적 | `weakref`, `sys.getrefcount` 활용 캐시 |

---

## 예시 코드
```python
box = LottoBox()

record = LottoRecord(
    round=1102,
    my_numbers={3, 8, 15, 22, 38, 44},
    winning_numbers=set(),  # 처음엔 비워두고 자동 추첨 대기
    matched_count=0,
    rank=""
)
# 새 회차 record 입력 시, winning_numbers 확정 및 등수 계산
box.append(record) 

print(box[0])                      # 인덱싱 확인
print(box.is_duplicate(1102))     # 1102회차 등록 여부
print(box.get_my_numbers(1102))   # 1102회차 구매 번호
print(box.export_bytes())         # 바이트 직렬화 출력
print(box.get_ref_count(record))  # 참조 수 확인
```

---

## 제출 조건
- 전체 코드는 하나의 Python 파일로 제출
- 제출 디렉토리는 현 디렉터리(study-fluent-python-2e/Assignment/) 입니다. 해당 경로에 커밋해 주세요.
- 파일명 양식 : part1_LottoBox_깃헙계정.py (ex. ** part1_LottoBox_jeongmo-bae.py ** 
- (선택) 주요 클래스 및 메서드에 주석 또는 docstring 포함
