import re
import cv2
import numpy as np
import base64
import io
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.base import ContentFile
from .models import Profile

class RegisterForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)  # File upload
    captured_image = forms.CharField(required=False)  # Base64 webcam capture
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        """ Process either uploaded image or captured image """
        cleaned_data = super().clean()
        profile_pic = cleaned_data.get("profile_pic")
        captured_image = cleaned_data.get("captured_image")

        if captured_image:
            try:
                # Convert Base64 string to an image file
                format, imgstr = captured_image.split(';base64,')  # Extract format and data
                ext = format.split('/')[-1]  # Get file extension
                image_data = base64.b64decode(imgstr)

                # Convert to Django-compatible file
                cleaned_data["profile_pic"] = ContentFile(image_data, name=f"profile.{ext}")

            except Exception:
                raise ValidationError("⚠ Error processing captured image. Please try again.")

        return cleaned_data

    def clean_profile_pic(self):
        """ Validate that the profile picture contains a visible human face """
        profile_pic = self.cleaned_data.get("profile_pic")

        if profile_pic:
            try:
                # Convert image to OpenCV format
                img = Image.open(profile_pic)
                img = img.convert("RGB")
                img_np = np.array(img)
                img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

                # Load OpenCV's pre-trained face detector
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

                # Detect faces
                faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) == 0:
                    raise ValidationError("⚠ Profile picture must contain a visible human face.")

            except Exception:
                raise ValidationError("⚠ Invalid image format. Please upload a clear photo with a visible human face.")

        return profile_pic
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'address', 'profile_picture']