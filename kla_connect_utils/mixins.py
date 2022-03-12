class GetCurrentUserAnnotatedSerializerMixin(object):
    """
    Get current user from context
    """

    def get_current_user(self):
        request = self.context.get("request", None)
        if request:
            user = getattr(request, "user", None)
            if user and user.is_authenticated:
                return user
        return None