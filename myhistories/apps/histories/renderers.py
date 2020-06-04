from ..core.renderers import GenericJSONRenderer


class HistoryJSONRenderer(GenericJSONRenderer):
    object_label = "history"
    pagination_object_label = "histories"
    pagination_count_label = "historiesCount"


class CommentJSONRenderer(GenericJSONRenderer):
    object_label = "comment"
    pagination_object_label = "comments"
    pagination_count_label = "commentsCount"
