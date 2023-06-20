from rest_framework import permissions


class IsAuthenticatedOrReadOnlyExceptBookMark(permissions.BasePermission):
    """IsAuthenticatedOrReadOnlyExceptBookMark

    북마크 조회를 제외한 GET요청은 비로그인시에도 요청가능합니다.
    북마크 조회와 기타 요청(POST)는 로그인이 필요합니다.
    """

    def has_permission(self, request, view):
        if (
            request.GET.get("filter") == "bookmarked"
            or request.method not in permissions.SAFE_METHODS
        ):
            return bool(request.user and request.user.is_authenticated)
        return True
