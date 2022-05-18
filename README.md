# Notes
## [Django-based](https://www.djangoproject.com/) web application to create post and share notes
***
https://notes.zoloto.cx.ua/
***

Requires registration and login to create, edit and delete notes.
All notes are associated with a user.
Every note can be shared thus making it accessible to everyone.
Shared notes can be liked by the registered users.
Homepage displays shared notes sorted by the [amount of likes](https://notes.zoloto.cx.ua/) or
 [creation date](https://notes.zoloto.cx.ua/?sort=date). Registration is not required to view public notes.

Note creation and editing is provided with a rich text editor [TinyMCE](https://pypi.org/project/django-tinymce/).\
Note body contains html but it is always sanitized using [tinyMCE](https://pypi.org/project/django-tinymce/) (both during frontend and form validation) or
 [bleach](https://pypi.org/project/bleach/) library if the note is created by API.

Supports all four [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) 
[JSON](https://www.json.org/json-en.html) encoded API methods such as GET POST PUT and DELETE.\
more information with examples: https://notes.zoloto.cx.ua/api

Public notes are accessed via an API and do not require authentication; private, on the other hand, can be accessed via
 [Session](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication) or 
[Token](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) authentication.\
Token can be generated on the [profile](https://notes.zoloto.cx.ua/profile) page.
***

Web application consists of:
- [homepage](https://notes.zoloto.cx.ua/) that displays public notes  
- [login](https://notes.zoloto.cx.ua/login) and [registration](https://notes.zoloto.cx.ua/register) pages
- [notes list page](https://notes.zoloto.cx.ua/notes) to view user's notes
- [note](https://notes.zoloto.cx.ua/notes/1017) details page
- [note creation and editing](https://notes.zoloto.cx.ua/notes/1017) page
- [profile page](https://notes.zoloto.cx.ua/profile) shows user information, allows it to
 change and shows stats about user activity
- [API page](https://notes.zoloto.cx.ua/api)
