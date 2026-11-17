<<<<<<< HEAD
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
=======
import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]

        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제가 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if not isinstance(answer, int) or answer < 1 or answer > 4:
            raise ValueError("정답 번호는 1~4여야 합니다.")

        return Quiz(question, choices, answer)


def create_default_quizzes():
    return [
        Quiz(
            "Python의 창시자는?",
            ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"],
            1,
        ),
        Quiz(
            "Python에서 화면에 글자를 출력하는 함수는?",
            ["echo()", "print()", "write()", "show()"],
            2,
        ),
        Quiz(
            "Python에서 정수를 나타내는 자료형은?",
            ["str", "bool", "int", "list"],
            3,
        ),
        Quiz(
            "Python에서 여러 값을 순서대로 담는 자료형은?",
            ["list", "int", "bool", "float"],
            1,
        ),
        Quiz(
            "Python에서 함수를 만들 때 사용하는 키워드는?",
            ["function", "func", "make", "def"],
            4,
        ),
    ]


def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()

        if text == "":
            print(f"⚠️ 입력이 비어 있습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        if number < minimum or number > maximum:
            print(f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
            continue

        return number


def read_text(prompt):
    while True:
        text = input(prompt).strip()

        if text == "":
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")
            continue

        return text


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()

    def load_state(self):
        if not STATE_FILE.exists():
            self.quizzes = create_default_quizzes()
            self.best_score = None
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]

            best = data["best_score"]
            if best is not None:
                best = {
                    "score": int(best["score"]),
                    "correct": int(best["correct"]),
                    "total": int(best["total"]),
                }
            self.best_score = best

            print(
                f"📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개)"
            )
        except (OSError, ValueError, KeyError, TypeError):
            print("⚠️ 저장 파일을 읽을 수 없어 기본 데이터로 초기화합니다.")
            self.quizzes = create_default_quizzes()
            self.best_score = None
            self.save_state()

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 파일 저장에 실패했습니다.")

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct_count = 0

        print()
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print()
            print("-" * 40)
            print(f"[문제 {number}]")
            quiz.display()
            print()

            user_answer = read_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = correct_count * 100 // total

        print()
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        result = {"score": score, "correct": correct_count, "total": total}
        self.update_best_score(result)

    def update_best_score(self, result):
        if self.best_score is None or result["score"] > self.best_score["score"]:
            self.best_score = result
            self.save_state()
            print("🎉 새로운 최고 점수입니다!")

        print("=" * 40)

    def add_quiz(self):
        print()
        print("📌 새로운 퀴즈를 추가합니다.")
        print()

        question = read_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, 5):
            choice = read_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = read_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()

        print()
        print("✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        print()
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print()
        print("-" * 40)

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

        print("-" * 40)

    def show_best_score(self):
        print()
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.")
            return

        print(
            f"🏆 최고 점수: {self.best_score['score']}점 "
            f"({self.best_score['total']}문제 중 {self.best_score['correct']}문제 정답)"
        )

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                    print()
                elif choice == 2:
                    self.add_quiz()
                    print()
                elif choice == 3:
                    self.show_quiz_list()
                    print()
                elif choice == 4:
                    self.show_best_score()
                    print()
                elif choice == 5:
                    self.save_state()
                    print("👋 프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            self.save_state()
            print()
            print("👋 입력이 중단되어 저장 후 안전하게 종료합니다.")


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
>>>>>>> c95b8f257410c72fd47e86bc05ef9993d4f6e725
