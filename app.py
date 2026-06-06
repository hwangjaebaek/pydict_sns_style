from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY", "pydict-secret-2024")

GRAMMAR_DATA = [
    {
        "slug": "variables", "keyword": "변수", "title": "변수와 자료형",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "값을 저장하는 이름표. 선언 없이 대입하면 자동 생성됩니다.",
        "preview_code": "name = '홍길동'\nage  = 20\ngpa  = 3.75",
        "likes": 247, "version_added": "1.0",
    },
    {
        "slug": "print", "keyword": "print()", "title": "출력 함수",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "화면에 값을 출력합니다. f-string으로 변수를 섞어 쓸 수 있어요.",
        "preview_code": 'print(f"이름: {name}, 나이: {age}")',
        "likes": 183, "version_added": "1.0",
    },
    {
        "slug": "input", "keyword": "input()", "title": "사용자 입력",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "키보드로 입력을 받습니다. 항상 str로 반환되므로 형변환 필요.",
        "preview_code": 'age = int(input("나이: "))',
        "likes": 156, "version_added": "1.0",
    },
    {
        "slug": "if", "keyword": "if / elif / else", "title": "조건문",
        "category": "control", "category_label": "제어문", "level": "basic",
        "summary": "조건이 참일 때만 코드를 실행합니다. 들여쓰기로 블록을 구분해요.",
        "preview_code": "if score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')",
        "likes": 312, "version_added": "1.0",
    },
    {
        "slug": "for", "keyword": "for", "title": "for 반복문",
        "category": "control", "category_label": "제어문", "level": "basic",
        "summary": "리스트, range 등 반복 가능한 객체를 순서대로 순회합니다.",
        "preview_code": "for i in range(5):\n    print(i)",
        "likes": 428, "version_added": "1.0",
    },
    {
        "slug": "while", "keyword": "while", "title": "while 반복문",
        "category": "control", "category_label": "제어문", "level": "basic",
        "summary": "조건이 참인 동안 계속 반복합니다. break로 탈출 가능.",
        "preview_code": "while count < 5:\n    count += 1",
        "likes": 198, "version_added": "1.0",
    },
    {
        "slug": "def", "keyword": "def", "title": "함수 정의",
        "category": "function", "category_label": "함수", "level": "basic",
        "summary": "코드를 재사용 가능한 단위로 묶습니다. return으로 결과를 돌려줘요.",
        "preview_code": "def greet(name):\n    return f'안녕, {name}!'",
        "likes": 356, "version_added": "1.0",
    },
    {
        "slug": "lambda", "keyword": "lambda", "title": "람다 함수",
        "category": "function", "category_label": "함수", "level": "mid",
        "summary": "한 줄짜리 익명 함수. sorted, map, filter와 자주 함께 씁니다.",
        "preview_code": "square = lambda x: x ** 2",
        "likes": 201, "version_added": "1.0",
    },
    {
        "slug": "list", "keyword": "[ ]", "title": "리스트",
        "category": "data", "category_label": "자료구조", "level": "basic",
        "summary": "순서 있는 데이터 묶음. 추가·삭제·수정이 자유롭습니다.",
        "preview_code": 'fruits = ["사과", "바나나", "포도"]\nfruits.append("망고")',
        "likes": 389, "version_added": "1.0",
    },
    {
        "slug": "dict", "keyword": "{ }", "title": "딕셔너리",
        "category": "data", "category_label": "자료구조", "level": "basic",
        "summary": "키-값 쌍으로 데이터를 저장합니다. 키로 빠르게 조회 가능.",
        "preview_code": 'student = {"name": "홍길동", "age": 20}',
        "likes": 341, "version_added": "1.0",
    },
    {
        "slug": "class", "keyword": "class", "title": "클래스",
        "category": "oop", "category_label": "객체지향", "level": "mid",
        "summary": "속성과 메서드를 묶는 설계도. 인스턴스를 생성해서 사용합니다.",
        "preview_code": "class Student:\n    def __init__(self, name):\n        self.name = name",
        "likes": 276, "version_added": "1.0",
    },
    {
        "slug": "int", "keyword": "int()", "title": "정수 형변환",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "문자열이나 실수를 정수로 변환합니다. 소수점은 버림 처리됩니다.",
        "preview_code": "int('42')   # 42\nint(3.9)    # 3 (버림)",
        "likes": 134, "version_added": "1.0",
    },
    {
        "slug": "float", "keyword": "float()", "title": "실수 형변환",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "문자열이나 정수를 실수(float)로 변환합니다.",
        "preview_code": "float('3.14')  # 3.14\nfloat(5)       # 5.0",
        "likes": 112, "version_added": "1.0",
    },
    {
        "slug": "str", "keyword": "str()", "title": "문자열 형변환",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "숫자 등 다른 자료형을 문자열로 변환합니다.",
        "preview_code": "str(100)          # '100'\n'결과: ' + str(99)  # '결과: 99'",
        "likes": 98, "version_added": "1.0",
    },
    {
        "slug": "operators", "keyword": "// % **", "title": "산술 연산자",
        "category": "basic", "category_label": "기초 문법", "level": "basic",
        "summary": "몫(//)·나머지(%)·거듭제곱(**) 등 파이썬의 특수 산술 연산자입니다.",
        "preview_code": "10 // 3   # 3\n10 % 3    # 1\n2 ** 10   # 1024",
        "likes": 167, "version_added": "1.0",
    },
    {
        "slug": "range", "keyword": "range()", "title": "범위 생성",
        "category": "control", "category_label": "제어문", "level": "basic",
        "summary": "정수 범위를 생성합니다. range(m, n, step)으로 시작·끝·간격을 지정합니다.",
        "preview_code": "list(range(5))        # [0,1,2,3,4]\nlist(range(0,10,2))   # [0,2,4,6,8]",
        "likes": 289, "version_added": "1.0",
    },
    {
        "slug": "in", "keyword": "in", "title": "포함 확인",
        "category": "control", "category_label": "제어문", "level": "basic",
        "summary": "리스트·문자열 등에 값이 포함되어 있는지 True/False로 반환합니다.",
        "preview_code": "3 in [1,2,3]     # True\n'a' in 'abc'     # True",
        "likes": 215, "version_added": "1.0",
    },
    {
        "slug": "args", "keyword": "*args", "title": "가변 매개변수",
        "category": "function", "category_label": "함수", "level": "mid",
        "summary": "개수가 정해지지 않은 인수를 튜플로 받습니다. sum 등과 함께 자주 씁니다.",
        "preview_code": "def total(*args):\n    return sum(args)\ntotal(1,2,3)   # 6",
        "likes": 178, "version_added": "1.0",
    },
    {
        "slug": "global", "keyword": "global", "title": "전역변수 수정",
        "category": "function", "category_label": "함수", "level": "mid",
        "summary": "함수 안에서 전역변수를 수정할 때 global 키워드를 선언해야 합니다.",
        "preview_code": "count = 0\ndef up():\n    global count\n    count += 1",
        "likes": 143, "version_added": "1.0",
    },
    {
        "slug": "recursive", "keyword": "재귀 함수", "title": "재귀 함수",
        "category": "function", "category_label": "함수", "level": "mid",
        "summary": "함수가 자기 자신을 호출합니다. 반드시 종료 조건(base case)이 필요합니다.",
        "preview_code": "def fact(n):\n    if n <= 1: return 1\n    return n * fact(n-1)",
        "likes": 231, "version_added": "1.0",
    },
    {
        "slug": "encapsulation", "keyword": "__변수명", "title": "캡슐화 / 정보 은닉",
        "category": "oop", "category_label": "객체지향", "level": "mid",
        "summary": "이중 언더스코어로 시작하는 변수는 외부에서 직접 접근이 불가합니다. getter/setter로 제어합니다.",
        "preview_code": "class Person:\n    def __init__(self):\n        self.__age = 0\n    def get_age(self): return self.__age",
        "likes": 189, "version_added": "1.0",
    },
    {
        "slug": "inheritance", "keyword": "class 자식(부모)", "title": "상속",
        "category": "oop", "category_label": "객체지향", "level": "mid",
        "summary": "부모 클래스의 속성과 메서드를 물려받습니다. super()로 부모 생성자를 호출합니다.",
        "preview_code": "class Cat(Animal):\n    def __init__(self, name):\n        super().__init__(name)\n    def speak(self): return '야옹'",
        "likes": 254, "version_added": "1.0",
    },
    {
        "slug": "file-open", "keyword": "open()", "title": "파일 열기",
        "category": "file", "category_label": "파일", "level": "mid",
        "summary": "파일을 열어 읽거나 씁니다. with 문을 쓰면 자동으로 닫힙니다.",
        "preview_code": "with open('file.txt', 'r') as f:\n    data = f.read()",
        "likes": 203, "version_added": "1.0",
    },
    {
        "slug": "pickle", "keyword": "pickle", "title": "피클 (객체 저장)",
        "category": "file", "category_label": "파일", "level": "mid",
        "summary": "파이썬 객체를 파일에 저장(dump)하고 불러옵니다(load). 바이너리 모드 필수.",
        "preview_code": "import pickle\nwith open('d.pkl','wb') as f:\n    pickle.dump(data, f)",
        "likes": 156, "version_added": "1.0",
    },
    {
        "slug": "import", "keyword": "import", "title": "모듈 불러오기",
        "category": "module", "category_label": "모듈", "level": "basic",
        "summary": "외부 모듈을 불러옵니다. as로 별칭을 붙이거나 from으로 일부만 가져올 수 있어요.",
        "preview_code": "import math\nfrom math import sqrt\nsqrt(25)   # 5.0",
        "likes": 198, "version_added": "1.0",
    },
    {
        "slug": "os", "keyword": "os", "title": "os 모듈",
        "category": "module", "category_label": "모듈", "level": "mid",
        "summary": "운영체제 관련 기능을 제공합니다. 경로 확인·폴더 탐색 등에 사용합니다.",
        "preview_code": "import os\nos.getcwd()\nos.listdir('.')",
        "likes": 167, "version_added": "1.0",
    },
]

SECTIONS_META = {
    "basic":    {"name": "기초 문법",  "icon": "📝"},
    "control":  {"name": "제어문",    "icon": "🔀"},
    "function": {"name": "함수",      "icon": "⚙️"},
    "data":     {"name": "자료구조",  "icon": "🗂️"},
    "oop":      {"name": "객체지향",  "icon": "🧩"},
    "file":     {"name": "파일",      "icon": "📁"},
    "module":   {"name": "모듈",      "icon": "📦"},
}


@app.context_processor
def inject_session_data():
    return {
        "history_list": session.get("history", []),
        "favorite_list": session.get("favorites", []),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    error_msg = None
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if keyword:
            q = keyword.lower()
            results = [
                g for g in GRAMMAR_DATA
                if q in g["keyword"].lower() or q in g["title"].lower() or q in g["slug"].lower()
            ]
            if not results:
                error_msg = f"'{keyword}'에 해당하는 문법을 찾을 수 없습니다."
            else:
                history = session.get("history", [])
                if keyword in history:
                    history.remove(keyword)
                history.insert(0, keyword)
                session["history"] = history[:10]
                session.modified = True
                return redirect(url_for("search") + f"?q={keyword}")

    selected_cat = request.args.get("cat", "")
    items = GRAMMAR_DATA if not selected_cat else [
        g for g in GRAMMAR_DATA if g["category"] == selected_cat
    ]
    return render_template(
        "index.html",
        all_items=items,
        selected_cat=selected_cat,
        total_count=len(GRAMMAR_DATA),
        error_msg=error_msg,
    )


@app.route("/toggle_favorite/<word>", methods=["POST"])
def toggle_favorite(word):
    favorites = session.get("favorites", [])
    if word in favorites:
        favorites.remove(word)
    else:
        favorites.append(word)
    session["favorites"] = favorites
    session.modified = True
    return redirect(url_for("index"))


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if query:
        q = query.lower()
        results = [
            g for g in GRAMMAR_DATA
            if q in g["keyword"].lower()
            or q in g["title"].lower()
            or q in g["summary"].lower()
            or q in g["slug"].lower()
        ]
        if results:
            history = session.get("history", [])
            if query in history:
                history.remove(query)
            history.insert(0, query)
            session["history"] = history[:10]
            session.modified = True
    else:
        results = []
    suggestions = ["for", "if", "def", "list", "dict", "class", "while"]
    return render_template("search.html", query=query, results=results, suggestions=suggestions)


@app.route("/detail/<slug>")
def detail(slug):
    item = next((g for g in GRAMMAR_DATA if g["slug"] == slug), None)
    if item is None:
        return redirect(url_for("index"))

    idx = GRAMMAR_DATA.index(item)
    prev_item = GRAMMAR_DATA[idx - 1] if idx > 0 else None
    next_item = GRAMMAR_DATA[idx + 1] if idx < len(GRAMMAR_DATA) - 1 else None

    grammar = {
        **item,
        "view_count": str(item["likes"] * 6),
        "like_count": str(item["likes"]),
        "save_count": str(item["likes"] // 3),
        "description": item["summary"],
        "syntax": item.get("preview_code", ""),
        "examples": [],
        "notes": [],
        "related": [],
        "prev": {"slug": prev_item["slug"], "title": prev_item["title"]} if prev_item else None,
        "next": {"slug": next_item["slug"], "title": next_item["title"]} if next_item else None,
    }
    return render_template("detail.html", grammar=grammar)


if __name__ == "__main__":
    app.run(debug=True)
