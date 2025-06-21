from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
import uuid

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на чтение для всех пользователей,
    но только администраторы могут создавать/редактировать/удалять.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ImageHandlingMixin:
    """
    Миксин для обработки изображений в API
    """
    parser_classes = (MultiPartParser, FormParser)

    def handle_image(self, image_data):
        """
        Обработка изображения из base64 или файла
        """
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            # Обработка base64 изображения
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=filename)
            return default_storage.save(f'products/{filename}', data)
        elif hasattr(image_data, 'file'):
            # Обработка загруженного файла
            filename = f"{uuid.uuid4()}.{image_data.name.split('.')[-1]}"
            return default_storage.save(f'products/{filename}', image_data)
        return None

    def perform_create(self, serializer):
        """
        Переопределение метода создания для обработки изображения
        """
        image_data = self.request.data.get('photo')
        if image_data:
            image_path = self.handle_image(image_data)
            serializer.save(photo=image_path)
        else:
            serializer.save()

    def perform_update(self, serializer):
        """
        Переопределение метода обновления для обработки изображения
        """
        image_data = self.request.data.get('photo')
        if image_data:
            image_path = self.handle_image(image_data)
            serializer.save(photo=image_path)
        else:
            serializer.save() 