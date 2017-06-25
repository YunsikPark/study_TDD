from django.core.urlresolvers import resolve
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