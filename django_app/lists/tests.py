from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

# home_page는 어떤 함수일까 곧 작성하게 될 뷰 함수로 HTML을 반환한다.
# import 처리부분을 보면 알 수 있지만 이 함수를 lists/view.py파일에 저장할 계획이다.
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # resolve는 Django가 내부적으로 사용하는 함수로 URL을 해석해서 일치하는 뷰 함수를 찾는다.
        # 여기서는 '/'(사이트 루트가 호출될 때 resolve를 실행해서  home_page라는 함수를 호출한다.
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # HttpRequest객체를 생성해서 사용자가 어떤 요청을 브라우저에 보내는지 확인한다
        request = HttpRequest()
        # 이것을 home_page 뷰에 전달해서 응답을 취득한다 이 객체는 HttpResponse라는 클래스의 인스턴스다
        # 응답내용(HTML 형태로 사용자에게 보내는 것)이 특정 속성을 가지고 있는지 확인한다.
        response = home_page(request)
        # 그 다음은 응답내용이 <html>으로 시작하고 </html>으로 끝나는지 확인한다.
        # response.content는 byte형 데이터로 파이썬 문자열이 아니다. 따라서 b''구문을 사용해서 비교한다.
        # 자세한 내용은 Django페이지의 Porting to Python3자료를 참고
        # https://docs.djangoproject.com/en/1.11/topics/python3/
        self.assertTrue(response.content.startswith(b'<html>'))
        # 반환내용의 <title>태그에 "To-Do lists"라는 단어가 있는지 확인한다
        # 앞선 기능 테스트에서 확인한것이기 때문에 단위테스트도 확인해주어야 한다.
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)