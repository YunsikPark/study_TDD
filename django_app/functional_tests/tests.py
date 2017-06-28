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
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        # (에디스는 매우 체계적인 사람이다)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 다시 갱신되고, 두개 아이템이 목록에 보인다
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 새로운 사용자인 프란시스가 사이트에 접속한다

        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
        ## 쿠키를 통해 유입되는 것을 방지한다
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 프란시스가 홈페이지에 접속한다
        # 에디서의 리스트는 보이지 않는다
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다
        # 그는 에디스보다 재미가 없다
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득한다
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 임력한 흔적이 없다는 것을 다시 확인한다
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy milk', page_text)

        # 둘 다 만족하고 잠자리에 든다
