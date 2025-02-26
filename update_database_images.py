import os
import django
import sys
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reva_web.settings')
django.setup()

# Set up console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from viwe_pro.models import Products

def update_database_images():
    # Get the products directory path
    media_root = os.path.join(settings.BASE_DIR, 'media')
    products_dir = os.path.join(media_root, 'products')
    
    # Get list of actual files in the products directory
    actual_files = set(os.listdir(products_dir))
    
    # Get all products from database
    products = Products.objects.all()
    
    updated_count = 0
    errors_count = 0
    
    for product in products:
        try:
            if product.pro_photo:
                # Get current filename from database
                current_db_filename = os.path.basename(product.pro_photo.name)
                
                # If the current database filename exists in actual files, it's already correct
                if current_db_filename in actual_files:
                    print(f"✓ Already correct: {current_db_filename}")
                    continue
                
                # Try to find the corresponding file in actual files
                # First, try case-insensitive match
                matching_files = [f for f in actual_files if f.lower() == current_db_filename.lower()]
                
                if matching_files:
                    # Update database reference
                    new_filename = matching_files[0]
                    product.pro_photo.name = f"products/{new_filename}"
                    product.save()
                    print(f"✓ Updated: {current_db_filename} -> {new_filename}")
                    updated_count += 1
                else:
                    print(f"✗ Error: Could not find matching file for {current_db_filename}")
                    errors_count += 1
                    
        except Exception as e:
            print(f"✗ Error processing product {product.pro_name}: {str(e)}")
            errors_count += 1
    
    print("\nSummary:")
    print(f"Total products processed: {products.count()}")
    print(f"Successfully updated: {updated_count}")
    print(f"Errors encountered: {errors_count}")

if __name__ == "__main__":
    print("Starting database image reference update...")
    update_database_images()
    print("\nDatabase update completed!")
