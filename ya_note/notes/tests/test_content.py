from django.test import TestCase
from django.urls import reverse

from .constants import User
from notes.models import Note


class TestDetailNote(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='note_slug',
        )

    def test_user_notes_list(self):
        note_in_list_for_user = (
            (self.author, True),
            (self.reader, False),
        )
        for user, note_in_list in note_in_list_for_user:
            self.client.force_login(user)
            with self.subTest(user=user):
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, note_in_list)

    def test_add_and_edit_forms(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
