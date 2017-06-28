from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# unittest.TestCase를 상속해서 테스트를 클래스 형태로 만든다.
class NewVisitorTest(LiveServerTestCase):
    # setUp과 tearDown은 특수한 메소드로 각 테스트 시작 전과 후에 실행된다.
    # 필자는 브라우저를 시작하고 닫을 때 사용하고 있다
    # try/except과 비슷한 구조로 테스트에 에러가 발생해도 tearDown이 실행된다
    # 이를 이용하면 브라우저 창이 쓸데 없이 떠다니는 것을 막을 수 있다.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # 테스트 메인 코드는 test_can_start_a_list_and_retrieve_it_later라는 메소드다.
    # test라는 명칭으로 시작하는 모든 메소드는 테스트메소드이며 테스트 실행자에 의해 실행된다
    # 클래스당 하나 이상의 테스트 메소드를 작성할 수 있다
    # 가능한 테스트 내용을 알 수 있는 테스트 메소드 명칭을 사용하는 것이 좋다.
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스Edith)는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다
        # 테스트 어설션을 만들기 위해, assert 대신에 self.assertIn을 사용한다.
        # unittest는 테스트 어설션을 만들기 위해 이런 유용한 함수를 다수 제공한다.
        # 예를 들면 assertEqual, assertTrue, assertFalse같은 것이 있다.
        # 자세한 사항은 unittest온라인 문서를 확인하다
        # (https://docs.python.org/3/library/unittest.html)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy peacock feathers')
        # 엔터키를 치면 페이지가 갱신되고 작업목록에
        # "1: 공작깃털사기"아이템이 추가된다
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        # (에디스는 매우 체계적인 사람이다)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 다시 갱신되고, 두개 아이템이 목록에 보인다
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다
        # 사이트는 그녀를 위한 특정 URL을 생성해준다
        # 이 때 URL에 대한 설명도 함께 제공된다
        self.fail('Finish the test!')

        # 만족하고 잠자리에 든다

    # 마지막은 if __name__ == '__main__'부분이다(파이썬 스크립트가 다른 스크립트에 임포트된 것이 아니라
    # 커맨드라인을 통해 실행됐다는 것을 확인하는 코드다.
    # unittest.main()을 호출해서 unittest 테스트 실행자를 가동한다.
    # 이것은 자동으로 파일 내 테스트 클래스와 메소드를 찾아서 실행해 주는 역할을 한다.
    # if __name__ == '__main__':
    # warnings = 'ignore'는 테스트 작성 시에 발생하는 불필요한 리소스 경고를 제거하기 위한 것이다
    # 이 부분을 읽을 때쯤이면 이미 리소스 경고 문제가 발생하지 않기 때문에 삭제해도 상관없다.
    # unittest.main(warnings='ignore')
