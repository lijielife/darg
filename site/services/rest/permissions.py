from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Only can access non-destructive methods (like GET and HEAD)"""
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class UserCanAddCompanyPermission(SafeMethodsOnlyPermission):
    """Allow everyone which is not a shareholder nor an operator yet to add a company"""
    def has_object_permission(self, request, view, obj=None):

        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddCompanyPermission, self).has_object_permission(request, view, obj)


class UserCanEditCompanyPermission(permissions.BasePermission):
    """Allow everyone which is not a shareholder nor an operator yet to add a company"""
    def has_object_permission(self, request, view, obj=None):

        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(
            UserCanEditCompanyPermission, self
        ).has_object_permission(request, view, obj)


class UserIsOperatorPermission(permissions.BasePermission):
    """
    Only operators of the same company may edit
    """
    def has_object_permission(self, request, view, obj=None):

        if hasattr(obj, 'company'):
            company = obj.company
        elif hasattr(obj.buyer, 'company'):
            company = obj.buyer.company
        elif hasattr(obj.seller, 'company'):
            company = obj.seller.company

        return request.user.operator_set.filter(company=company).exists()


class UserCanAddShareholderPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):

        return request.user.operator_set.filter(company=obj.company).exists()


class UserCanAddPositionPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddPositionPermission, self).has_object_permission(request, view, obj)


class UserCanAddOptionPlanPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddOptionPlanPermission, self).has_object_permission(request, view, obj)


class UserCanAddOptionTransactionPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddOptionTransactionPermission, self).has_object_permission(request, view, obj)


class UserCanAddInviteePermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddInviteePermission, self).has_object_permission(request, view, obj)
