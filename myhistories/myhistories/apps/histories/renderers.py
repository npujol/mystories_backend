from myhistories.apps.core.renderers import ConduitJSONRenderer


class HistoryJSONRenderer(ConduitJSONRenderer):
    object_label = "history"
    pagination_object_label = "histories"
    pagination_count_label = "historiesCount"


class CommentJSONRenderer(ConduitJSONRenderer):
    object_label = "comment"
    pagination_object_label = "comments"
    pagination_count_label = "commentsCount"
