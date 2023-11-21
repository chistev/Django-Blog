This is a blog built with the Django Framework, Django Rest Framework, vanilla css, and vanilla javascript.

**THE IMPLEMENTED FEATURES INCLUDE:**

**For the accounts app**

1. A logged in user is unable to access the log in page.
2. Ability to log in and log out.
3. Ability to sign in if the user does not have an account.

![Login page](https://github.com/chistev/Django-Blog/assets/115540580/3ae66ba0-8cc1-4892-8cdd-7681c395f5b6)

**For the articles app**

1. The number of articles on the index page is limited to five at a time. When the number of articles exceeds 5, a pagination pops up.

   ![Screenshot 2023-11-17 105621](https://github.com/chistev/Django-Blog/assets/115540580/e66dccf2-25e8-4821-829f-03de3ecfc9d1)

2. Ability for logged in users to like and unlike posts and comments asynchronously (No page refresh) using FETCH API.
3. Maximum number of displayed comments after loading the detail page is 10. If number of available comments exceed 10, a "Load more comments" button pops up which when clicked, displays the next batch of 10 comments, asynchronously.

   ![Screenshot 2023-11-17 110300](https://github.com/chistev/Django-Blog/assets/115540580/a274189d-e600-43f3-997c-5183851ec9fc)

4. Ability to create (using a rich text editor), delete, and edit posts by the admin user who made the post (only admins can create posts).

   ![Screenshot 2023-11-17 111446](https://github.com/chistev/Django-Blog/assets/115540580/10a58a0e-394d-488b-bba8-156563df0f9b)


   ![Screenshot 2023-11-17 110554](https://github.com/chistev/Django-Blog/assets/115540580/6d47a1ce-d8d0-494d-8b4d-d8e9c1b442a4)

   ![Screenshot 2023-11-17 110620](https://github.com/chistev/Django-Blog/assets/115540580/255c6f29-511d-4535-9453-2b9fddb6a894)

6. Ability to like comments by logged in users asynchronously. Also ability by the user who made a comment to edit or delete it.

   ![Screenshot 2023-11-17 110849](https://github.com/chistev/Django-Blog/assets/115540580/5dec9638-33c9-45b9-b30f-3bb8b58e9400)

7. Ability to search for articles.
   ![Screenshot 2023-11-17 111041](https://github.com/chistev/Django-Blog/assets/115540580/4711660b-f571-417e-b4c9-4c961a76bcc2)

8. Ability to view articles under similar category.
   ![Screenshot 2023-11-17 111240](https://github.com/chistev/Django-Blog/assets/115540580/a45b30e9-804f-4acb-9631-df12d55c5715)


**Unimplemented features are:**
1. Sending links to users to make them confirm their email used for registration and to reset forgotten password. This could not be implemented because I couldn't find a free email service to use. Gmail wouldn't let me.

2. Asyncronous submission of comments only works when the number of existing comments exceeds 10, otherwise there is a redirection to a white json page before submitted comment is displayed.

3. Inability to implement a threaded comment system. Went with single parent comments instead, which is not ideal for fostering conversations in a blog.



For the markdown you need to install cdeditor. You can do this by going to your project root directory and then in the terminal -

> pip install django-ckeditor

in the settings.py, add
    
    'article',
    'account',
    'rest_framework'
    'ckeditor'

    to installed apps.

Also, add in your settings.py

    STATIC_URL = 'static/'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
    MEDIA_URL = '/images/'
