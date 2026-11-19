from query_processing.qpCore import Search
from query_processing.parsing.parse_url import find_id, get_answer_id, get_answer
from app.on_startup import on_startup
import html
import re
from query_processing.qp_on_startup import proceed_unencoded

engine = Search()



CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def format_so_answer(raw_html: str) -> str:
    text = html.unescape(raw_html)

    def style_code_block(match):
        code = match.group(1).strip("\n")
        lines = [f"  {GRAY}│{RESET} {GREEN}{line}{RESET}" for line in code.splitlines()]
        return "\n" + "\n".join(lines) + "\n"

    text = re.sub(r"<pre><code>(.*?)</code></pre>", style_code_block, text, flags=re.DOTALL)

    text = re.sub(r"<code>(.*?)</code>", rf"{YELLOW}\1{RESET}", text)

    text = re.sub(r'<a href="(.*?)".*?>(.*?)</a>', rf"{BOLD}\2{RESET} ({CYAN}\1{RESET})", text)

    text = re.sub(r"</p>\s*<p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)

    return text.strip()


def print_search_result(answer_html: str, link: str, score: float | None = None):
    score_str = f" {GRAY}| Match: {score:.2f}{RESET}" if score is not None else ""
    print(f"\n{CYAN}╭─ Similar question:{RESET} {BOLD}{link}{RESET}{score_str}")
    print(f"{CYAN}│{RESET}")
    
    formatted = format_so_answer(answer_html)
    for line in formatted.splitlines():
        print(f"{CYAN}│{RESET} {line}")
        
    print(f"{CYAN}╰{'─' * 65}{RESET}\n")


def main_loop():
    print("Search ready. Press CTRL+C or type 'q' to quit.\n")
    while True:
        try:
            usr_s = input("Enter your search -> ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        if not usr_s:
            continue
        if usr_s.lower() == 'q':
            print("\nExiting...")
            break
        url = engine.search(usr_s).get('db_url')
        answer = get_answer(get_answer_id(find_id(url=url)))
        p_answ = format_so_answer(answer)
        print_search_result(p_answ, link=url)

    

if __name__ == '__main__':
    if on_startup():
        proceed_unencoded()
        main_loop()
        