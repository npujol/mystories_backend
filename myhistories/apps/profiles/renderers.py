from ..core.renderers import GenericJSONRenderer


class ProfileJSONRenderer(GenericJSONRenderer):
    object_label = "profile"
    pagination_object_label = "profiles"
    pagination_count_label = "profilesCount"
