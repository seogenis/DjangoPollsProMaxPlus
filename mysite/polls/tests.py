# Create your tests here.
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice, ObjectLog
from django.urls import reverse
from .serializer import QuestionSerializer, ChoiceSerializer


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )



class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)



class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionModelTest(TestCase):
    def test_create_question(self):
        data = {'question_text': 'What is your favorite color?', 'pub_date': timezone.now()}
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        question = serializer.save()
        self.assertIsInstance(question, Question)
        self.assertEqual(question.question_text, 'What is your favorite color?')

    def test_update_question(self):
        question = Question.objects.create(question_text='What is your favorite color?', pub_date=timezone.now())
        data = {'question_text': 'What is your favorite animal?'}
        serializer = QuestionSerializer(instance=question, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_question = serializer.save()
        self.assertEqual(updated_question.question_text, 'What is your favorite animal?')
        self.assertEqual(ObjectLog.objects.filter(action='M', object_id=question.id).count(), 1)

    def test_delete_question(self):
        question = Question.objects.create(question_text='What is your favorite color?', pub_date=timezone.now())
        question_id = question.id
        question.delete()
        self.assertFalse(Question.objects.filter(id=question_id).exists())
        self.assertEqual(ObjectLog.objects.filter(action='D', object_id=question_id).count(), 1)

class ChoiceModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(question_text='What is your favorite color?', pub_date=timezone.now())

    def test_create_choice(self):
        data = {'question': self.question.id, 'choice_text': 'Blue', 'votes': 0}
        serializer = ChoiceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        choice = serializer.save()
        self.assertIsInstance(choice, Choice)
        self.assertEqual(choice.choice_text, 'Blue')

    def test_update_choice(self):
        choice = Choice.objects.create(question=self.question, choice_text='Blue', votes=0)
        data = {'choice_text': 'Red'}
        serializer = ChoiceSerializer(instance=choice, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_choice = serializer.save()
        self.assertEqual(updated_choice.choice_text, 'Red')
        self.assertEqual(ObjectLog.objects.filter(action='M', object_id=choice.id).count(), 1)

    def test_delete_choice(self):
        choice = Choice.objects.create(question=self.question, choice_text='Blue', votes=0)
        choice_id = choice.id
        choice.delete()
        self.assertFalse(Choice.objects.filter(id=choice_id).exists())
        self.assertEqual(ObjectLog.objects.filter(action='D', object_id=choice_id).count(), 1)