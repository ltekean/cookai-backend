from rest_framework.pagination import PageNumberPagination

"""
pagination을 커스텀 하거나, 필요한 곳에 지정하여 사용할 수 있습니다.
"""


class UserCommentPagination(PageNumberPagination):
    page_size = 4
    page_query_param = "page"
    max_page_size = 100


class UserFollowerPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "user_follower_page"
    max_page_size = 100


class UserFollowingPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "user_following_page"
    max_page_size = 100
