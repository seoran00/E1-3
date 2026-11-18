import time
import json


def mac(pattern, filt):
    n = len(pattern)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def read_row(prompt, size):
    while True:
        text = input(prompt)
        parts = text.split()

        if len(parts) != size:
            print(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")
            continue

        try:
            row = []
            for p in parts:
                row.append(float(p))
            return row
        except ValueError:
            print(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")


def read_matrix(title, size):
    print(f"{title} ({size}줄 입력, 공백 구분)")
    matrix = []
    for i in range(size):
        row = read_row("", size)
        matrix.append(row)
    return matrix


EPSILON = 1e-9


def judge(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "판정 불가"
    if score_a > score_b:
        return "A"
    return "B"


def judge_label(cross_score, x_score):
    if abs(cross_score - x_score) < EPSILON:
        return "UNDECIDED"
    if cross_score > x_score:
        return "Cross"
    return "X"


def measure_mac(pattern, filt, repeat=10):
    total_ms = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        end = time.perf_counter()
        total_ms += (end - start) * 1000
    return total_ms / repeat


def make_matrix(n, value=1.0):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(value)
        matrix.append(row)
    return matrix


def print_performance(sizes=(3, 5, 13, 25)):
    print()
    print("#---------------------------------------")
    print("# 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<10}{'평균 시간(ms)':<18}{'연산 횟수(N²)':<10}")
    print("-" * 40)
    for n in sizes:
        pattern = make_matrix(n)
        filt = make_matrix(n)
        avg_ms = measure_mac(pattern, filt)
        print(f"{str(n) + '×' + str(n):<10}{avg_ms:<18.4f}{n * n:<10}")


def run_mode1():
    print("#----------------------------------------")
    print("# [1] 필터 입력")
    print("#----------------------------------------")
    filter_a = read_matrix("필터 A", 3)
    filter_b = read_matrix("필터 B", 3)

    print("#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")
    pattern = read_matrix("패턴", 3)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    print("#----------------------------------------")
    print("# [3] MAC 결과")
    print("#----------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    avg_ms = measure_mac(pattern, filter_a)
    print(f"연산 시간(평균/10회): {avg_ms:.3f} ms")
    print(f"판정: {judge(score_a, score_b)}")
    print_performance(sizes=(3,))


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_label(label):
    text = str(label).strip().lower()
    if text in ("+", "cross"):
        return "Cross"
    if text == "x":
        return "X"
    return None


def extract_size(name):
    parts = name.split("_")
    if len(parts) != 3 or parts[0] != "size":
        return None
    if not parts[1].isdigit():
        return None
    return int(parts[1])
    

def run_mode2():
    data = load_data("data.json")
    filters = data["filters"]
    patterns = data["patterns"]

    total = 0
    passed = 0
    failures = []

    for name, item in patterns.items():
        total += 1
        print(f"--- {name} ---")

        size = extract_size(name)
        filter_group = filters.get(f"size_{size}")
        if filter_group is None:
            print("FAIL: 해당 크기의 필터가 없습니다.")
            failures.append((name, "해당 크기의 필터 없음"))
            continue

        pattern = item["input"]
        cross_score = mac(pattern, filter_group["cross"])
        x_score = mac(pattern, filter_group["x"])

        result = judge_label(cross_score, x_score)
        expected = normalize_label(item["expected"])

        print(f"Cross 점수: {cross_score}")
        print(f"X 점수: {x_score}")

        if result == expected:
            passed += 1
            print(f"판정: {result} | expected: {expected} | PASS")
        else:
            print(f"판정: {result} | expected: {expected} | FAIL")
            failures.append((name, f"판정 {result}, expected {expected}"))
     

    print_performance()


    print()
    print("# 결과 요약")
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {len(failures)}개")
    if failures:
        print("실패 케이스:")
        for name, reason in failures:
            print(f"- {name}: {reason}")


def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    while True:
        choice = input("선택: ").strip()
        if choice == "1":
            run_mode1()
            break
        if choice == "2":
            run_mode2()
            break
        print("입력 오류: 1 또는 2를 입력하세요.")


main()
