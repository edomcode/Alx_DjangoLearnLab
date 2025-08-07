Permissions and Groups Setup
Custom Permissions
Defined in 'Book' model:

can_view
can_create
can_edit
can_delete
Groups
Viewers: can_view
Editors: can_create, can_edit
Admins: All permissions
Usage
Decorators like @permission_required('book_content.can_edit') are used to enforce access to views.

Testing
Create users and assign them to groups using the Django Admin or shell.
Login as users and verify their access rights on views.