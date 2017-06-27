import re
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.models import Item

# home_page는 어떤 함수일까 곧 작성하게 될 뷰 함수로 HTML을 반환한다.
# import 처리부분을 보면 알 수 있지만 이 함수를 lists/view.py파일에 저장할 계획이다.
from lists.views import home_page


class HomePageTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_root_url_resolves_to_home_page_view(self):
        # resolve는 Django가 내부적으로 사용하는 함수로 URL을 해석해서 일치하는 뷰 함수를 찾는다.
        # 여기서는 '/'(사이트 루트가 호출될 때 resolve를 실행해서  home_page라는 함수를 호출한다.
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(
            re.sub(self.pattern_input_csrf, '', response.content.decode()),
            re.sub(self.pattern_input_csrf, '', expected_html)
        )

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string(
        #     'home.html',
        #     {
        #         'new_item_text': 'A new list item',
        #     }
        # )

        # self.assertEqual(
        #     re.sub(self.pattern_input_csrf, '', response.content.decode()),
        #     re.sub(self.pattern_input_csrf, '', expected_html)
        # )

        # self.assertEqual(
        #     re.sub(self.pattern_input_csrf, '', response.status_code, 302),
        #     re.sub(self.pattern_input_csrf, '', response['location'], '/')
        # )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
