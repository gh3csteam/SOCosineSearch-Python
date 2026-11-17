from query_processing.qpCore import Search
from query_processing.parsing.parse_url import find_id, get_answer_id, get_answer
engine = Search()

if __name__ == '__main__':
    url = engine.search().get('db_url')
    print(get_answer(get_answer_id(find_id(url=url))))
    print(f"simmilar question -> {url}")
    