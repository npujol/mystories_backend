from django.urls import reverse
from django.forms.models import model_to_dict

from rest_framework import status

from ..core.tests_utils import BaseRestTestCase

from .models import Comment, History, Tag, Speech
from .serializers import CommentSerializer, HistorySerializer, TagSerializer


class HistoryListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()

        self.url = reverse("histories:history-list")

    def test_create_history(self):
        histories_count = History.objects.all().count()

        response = self.client.post(
            self.url,
            {
                "title": "string",
                "body": "string for the body",
                "description": "string",
                "tagList": ["string"],
            },
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            History.objects.all().count(), (histories_count + 1),
        )
        self.assertEqual(History.objects.last().title, "string")

    def test_list_histories(self):
        """
        Test to verify histories list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(
            response.json().get("count"), History.objects.all().count(),
        )


class HistoryDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.history = History.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse(
            "histories:history-detail", kwargs={"slug": self.history.slug}
        )

    def test_history_object_detail(self):
        """
        Test to verify a history object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            HistorySerializer(instance=self.history).data, response.json(),
        )

    def test_history_object_update(self):
        response = self.client.put(
            self.url,
            {
                "title": "string",
                "body": "Another string for the body",
                "description": "string",
                "tagList": ["string"],
            },
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        history = History.objects.get(id=self.history.id)
        self.assertEqual(response.json().get("title"), history.title)

    def test_history_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"body": "another body"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        history = History.objects.get(id=self.history.id)
        self.assertEqual(response.json().get("body"), history.body)

    def test_history_object_delete(self):
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(204, response.status_code)


class TagListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("histories:tag-list")

    def test_create_tag(self):
        tags_count = Tag.objects.all().count()
        response = self.client.post(
            self.url, {"tag": "word"}, HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Tag.objects.all().count(), (tags_count + 1),
        )
        self.assertEqual(Tag.objects.last().tag, "word")

    def test_list_tags(self):
        """
        Test to verify the tags list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(
            response.json().get("count"), Tag.objects.all().count(),
        )


class TagDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(tag="word2")
        self.url = reverse("histories:tag-detail", kwargs={"pk": self.tag.pk})

    def test_tag_object_detail(self):
        """
        Test to verify a tag object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            TagSerializer(instance=self.tag).data, response.json(),
        )


class HistoryFavoriteAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.history = History.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse(
            "histories:history_favorite", kwargs={"history__slug": self.history.slug}
        )

    def test_favorite_history(self):
        """
        Test to favorite history
        """
        response = self.client.post(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(201, response.status_code)

    def test_unfavorite_history(self):
        """
        Test to unfavorite history
        """
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            HistorySerializer(instance=self.history).data, response.json(),
        )


class HistoriesFeedAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.history = History.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse("histories:histories_feed_list")

    def test_list_tags(self):
        """
        Test to verify the HistoriesFeed list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(
            response.json().get("count"), Tag.objects.all().count(),
        )


class CommentListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()

        self.history = History.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )

        self.url = reverse(
            "histories:comment_list", kwargs={"history__slug": self.history.slug}
        )

    def test_create_comment(self):
        comments_count = Comment.objects.all().count()

        response = self.client.post(
            self.url,
            {"body": "string for the body",},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Comment.objects.all().count(), (comments_count + 1),
        )
        self.assertEqual(Comment.objects.last().body, "string for the body")

    def test_list_comments(self):
        """
        Test to verify comments list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(
            response.json().get("count"), Comment.objects.all().count(),
        )


class CommentDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.history = History.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.comment = Comment.objects.create(
            author=self.user.profile, body="body for test", history=self.history,
        )
        self.url = reverse(
            "histories:comment_detail",
            kwargs={"pk": self.comment.pk, "history__slug": self.history.slug},
        )

    def test_comment_object_detail(self):
        """
        Test to verify a comment object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            CommentSerializer(instance=self.comment).data, response.json(),
        )

    def test_comment_object_delete(self):
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(204, response.status_code)


class HistoryGttsAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.history = History.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse(
            "histories:history_tts", kwargs={"history__slug": self.history.slug}
        )

    def test_add_gtts_history(self):
        """
        Test to create a speech from an history
        """
        response = self.client.post(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(202, response.status_code)

    def test_get_gtts_history(self):
        """
        Test to create a speech from an history
        """
        Speech.objects.create(history=self.history, language="en")

        response = self.client.get(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
