# import os
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse
# from rest_framework.test import APIClient, APITestCase
# from PIL import Image
# from .models import ImageUpload

# class ImageUploadTests(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
        
#         # 이미지 파일 생성
#         self.image = Image.new("RGB", (100, 100))
#         self.image_file = SimpleUploadedFile("test_image.jpg", content=b"test_image_content", content_type="image/jpeg")

#     def tearDown(self):
#         # 이미지 파일 삭제
#         for image in ImageUpload.objects.all():
#             if os.path.isfile(image.image.path):
#                 os.remove(image.image.path)

#     def test_image_upload(self):
#         # 이미지 업로드 API 호출
#         url = reverse("image_upload")
#         response = self.client.post(url, {"image": self.image_file}, format="multipart")
        
#         # 결과 확인
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("result", response.data)
#         self.assertTrue(ImageUpload.objects.filter(image="images/test_image.jpg").exists())
