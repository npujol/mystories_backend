from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status

from ..core.tests_utils import BaseRestTestCase
from .models import Comment, Speech, Story, Tag
from .serializers import CommentSerializer, StorySerializer, TagSerializer


class StoryListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()

        self.url = reverse("stories:story-list")

    def test_create_story(self):
        stories_count = Story.objects.all().count()

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
        self.assertEqual(Story.objects.all().count(), (stories_count + 1))
        self.assertEqual(Story.objects.last().title, "string")

    def test_list_stories(self):
        """
        Test to verify stories list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.json().get("count"), Story.objects.all().count())


class StoryDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.story = Story.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse("stories:story-detail", kwargs={"slug": self.story.slug})

    def test_story_object_detail(self):
        """
        Test to verify a story object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(StorySerializer(instance=self.story).data, response.json())

    def test_story_object_update(self):
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

        story = Story.objects.get(id=self.story.id)
        self.assertEqual(response.json().get("title"), story.title)

    def test_story_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"body": "another body"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        story = Story.objects.get(id=self.story.id)
        self.assertEqual(response.json().get("body"), story.body)

    def test_story_object_delete(self):
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(204, response.status_code)


class TagListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("stories:tag-list")

    def test_create_tag(self):
        tags_count = Tag.objects.all().count()
        response = self.client.post(
            self.url, {"tag": "word"}, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.all().count(), (tags_count + 1))
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

        self.assertEqual(response.json().get("count"), Tag.objects.all().count())


class TagDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(tag="word2")
        self.url = reverse("stories:tag-detail", kwargs={"pk": self.tag.pk})

    def test_tag_object_detail(self):
        """
        Test to verify a tag object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(TagSerializer(instance=self.tag).data, response.json())


class StoryFavoriteAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.story = Story.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse(
            "stories:story_favorite", kwargs={"story__slug": self.story.slug}
        )

    def test_favorite_story(self):
        """
        Test to favorite story
        """
        response = self.client.post(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(201, response.status_code)

    def test_unfavorite_story(self):
        """
        Test to unfavorite story
        """
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(StorySerializer(instance=self.story).data, response.json())


class StoriesFeedAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.story = Story.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse("stories:stories_feed_list")

    def test_list_tags(self):
        """
        Test to verify the StoriesFeed list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.json().get("count"), Tag.objects.all().count())


class CommentListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()

        self.story = Story.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )

        self.url = reverse(
            "stories:comment_list", kwargs={"story__slug": self.story.slug}
        )

    def test_create_comment(self):
        comments_count = Comment.objects.all().count()

        response = self.client.post(
            self.url,
            {"body": "string for the body"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.all().count(), (comments_count + 1))
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

        self.assertEqual(response.json().get("count"), Comment.objects.all().count())


class CommentDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.story = Story.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.comment = Comment.objects.create(
            author=self.user.profile, body="body for test", story=self.story
        )
        self.url = reverse(
            "stories:comment_detail",
            kwargs={"pk": self.comment.pk, "story__slug": self.story.slug},
        )

    def test_comment_object_detail(self):
        """
        Test to verify a comment object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(CommentSerializer(instance=self.comment).data, response.json())

    def test_comment_object_delete(self):
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(204, response.status_code)


class StoryGttsAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.story = Story.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            description="description for test",
        )
        self.url = reverse("stories:story_tts", kwargs={"story__slug": self.story.slug})

    def test_add_gtts_story(self):
        """
        Test to create a speech from a story
        """
        response = self.client.post(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(202, response.status_code)

    def test_get_gtts_story(self):
        """
        Test to create a speech from a story
        """
        Speech.objects.create(story=self.story, language="en")

        response = self.client.get(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
