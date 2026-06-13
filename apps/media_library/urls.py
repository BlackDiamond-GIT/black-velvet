from django.urls import path

from . import views

app_name = "media_library"

urlpatterns = [
    path("sign-upload/", views.sign_upload, name="sign_upload"),
    path("save-image/", views.save_image, name="save_image"),
    path("assign/<int:image_id>/", views.assign_image, name="assign_image"),
    path("unassign/<int:image_id>/", views.unassign_image, name="unassign_image"),
    path("picker/", views.image_picker, name="image_picker"),
]
