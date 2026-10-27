import os
import uuid
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from config import Config

class CloudinaryService:
    """Service to handle document and image uploads to Cloudinary with local storage fallback."""

    @staticmethod
    def _is_cloudinary_configured():
        """Check if valid Cloudinary credentials are set in environment configuration."""
        return bool(
            Config.CLOUDINARY_CLOUD_NAME and 
            Config.CLOUDINARY_API_KEY and 
            Config.CLOUDINARY_API_SECRET
        )

    @classmethod
    def upload_image(cls, file_obj, folder="hotel_management"):
        """
        Upload image or document file to Cloudinary cloud storage.
        If Cloudinary credentials are missing, falls back to saving locally in static/uploads/.
        Returns the secure URL string.
        """
        if not file_obj or not file_obj.filename:
            return ""

        filename = secure_filename(file_obj.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if ext not in Config.ALLOWED_EXTENSIONS:
            raise ValueError(f"File extension '.{ext}' is not allowed.")

        # If Cloudinary credentials are configured, upload to Cloudinary
        if cls._is_cloudinary_configured():
            try:
                cloudinary.config(
                    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
                    api_key=Config.CLOUDINARY_API_KEY,
                    api_secret=Config.CLOUDINARY_API_SECRET,
                    secure=True
                )
                upload_result = cloudinary.uploader.upload(
                    file_obj,
                    folder=f"hotel_management/{folder}",
                    resource_type="auto"
                )
                return upload_result.get("secure_url", "")
            except Exception as e:
                print(f"[!] Cloudinary Upload Failed ({e}). Falling back to local upload.")

        # Local Upload Fallback
        target_dir = os.path.join(Config.UPLOAD_FOLDER, folder)
        os.makedirs(target_dir, exist_ok=True)
        
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        save_path = os.path.join(target_dir, unique_name)
        
        # Reset file stream offset if read before
        file_obj.seek(0)
        file_obj.save(save_path)
        
        # Return web-accessible path
        return f"/static/uploads/{folder}/{unique_name}"
