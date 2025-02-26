import os
import django
import re
import sys
from django.conf import settings
from django.core.files import File

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reva_web.settings')
django.setup()

# Set up console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from viwe_pro.models import Products

def sanitize_filename(filename):
    # Remove the extension
    name, ext = os.path.splitext(filename)
    
    # Replace Arabic characters and spaces with English equivalents
    arabic_to_english = {
        'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'h', 'خ': 'kh',
        'د': 'd', 'ذ': 'th', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's',
        'ض': 'd', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q',
        'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'y',
        'أ': 'a', 'إ': 'e', 'آ': 'a', 'ة': 'h', 'ى': 'a', 'ئ': 'e'
    }
    
    # Replace Arabic characters
    for ar, en in arabic_to_english.items():
        name = name.replace(ar, en)
    
    # Replace spaces and special characters with underscores
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    
    # Remove multiple underscores
    name = re.sub(r'_+', '_', name)
    
    # Remove leading/trailing underscores
    name = name.strip('_')
    
    # Convert to lowercase
    name = name.lower()
    
    return f"{name}{ext}"

def rename_images():
    media_root = os.path.join(settings.BASE_DIR, 'media')
    products_dir = os.path.join(media_root, 'products')
    
    # Get all files in the products directory
    files = os.listdir(products_dir)
    
    # Create a mapping of old to new filenames
    filename_mapping = {}
    
    # First pass: generate new filenames and ensure uniqueness
    for old_filename in files:
        new_filename = sanitize_filename(old_filename)
        
        # Handle duplicates by adding a number
        base, ext = os.path.splitext(new_filename)
        counter = 1
        while new_filename in filename_mapping.values():
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
            
        filename_mapping[old_filename] = new_filename
    
    # Second pass: rename files and update database
    for old_filename in files:
        if old_filename in filename_mapping:
            new_filename = filename_mapping[old_filename]
            
            # Full paths
            old_path = os.path.join(products_dir, old_filename)
            new_path = os.path.join(products_dir, new_filename)
            
            try:
                # Rename the file
                os.rename(old_path, new_path)
                print(f"Renamed: {old_filename} -> {new_filename}")
                
                # Update database references if they exist
                products = Products.objects.filter(pro_photo__contains=old_filename)
                for product in products:
                    product.pro_photo.name = f"products/{new_filename}"
                    product.save()
                    print(f"Updated database reference for product {product.pro_name}")
                    
            except Exception as e:
                print(f"Error processing {old_filename}: {str(e)}")

if __name__ == "__main__":
    rename_images()
    print("Image renaming process completed!")
