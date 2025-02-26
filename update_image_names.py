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

def create_mapping():
    """Create a mapping between Arabic and English names"""
    mapping = {
        'فولتاك': 'voltac',
        'فولتك': 'voltac',
        'ريموكس': 'remoclav',
        'ريموكلاف': 'remoclav',
        'اندوميتاسين': 'indomethacin',
        'تيمبرو': 'tempro',
        'سيتامول': 'cetamol',
        'كوكسي': 'coxi',
        'بروفيو': 'profio',
        'سيلاكسين': 'celaxin',
        'مينسترال': 'minstral',
        'ريلاكسون': 'relaxon',
        'سيبرولوكس': 'ciprolox',
        # Add more mappings as needed
    }
    return mapping

def normalize_filename(filename):
    """Normalize filename by removing extension and converting to lowercase"""
    name = os.path.splitext(filename)[0].lower()
    return name

def find_matching_file(original_name, files_list, mapping):
    """Find a matching file from the files list using various methods"""
    original_base = normalize_filename(original_name)
    
    # Direct match
    for file in files_list:
        if normalize_filename(file) == original_base:
            return file
            
    # Try matching using the mapping
    for arabic, english in mapping.items():
        if arabic in original_base:
            for file in files_list:
                if english in normalize_filename(file):
                    return file
                    
    # Try matching numbers and partial matches
    numbers = ''.join(filter(str.isdigit, original_base))
    if numbers:
        for file in files_list:
            if numbers in ''.join(filter(str.isdigit, normalize_filename(file))):
                return file
                
    return None

def update_database_images():
    # Get the products directory path
    media_root = os.path.join(settings.BASE_DIR, 'media')
    products_dir = os.path.join(media_root, 'products')
    
    # Get list of actual files in the products directory
    actual_files = set(os.listdir(products_dir))
    
    # Create name mapping
    name_mapping = create_mapping()
    
    # Get all products from database
    products = Products.objects.all()
    
    updated_count = 0
    errors_count = 0
    skipped_count = 0
    
    print("Starting database update...")
    print(f"Total products to process: {products.count()}")
    
    for product in products:
        try:
            if product.pro_photo:
                current_db_filename = os.path.basename(product.pro_photo.name)
                
                # Skip if file already exists and matches
                if current_db_filename in actual_files:
                    print(f"✓ Already correct: {current_db_filename}")
                    skipped_count += 1
                    continue
                
                # Try to find matching file
                matching_file = find_matching_file(current_db_filename, actual_files, name_mapping)
                
                if matching_file:
                    # Update database reference
                    product.pro_photo.name = f"products/{matching_file}"
                    product.save()
                    print(f"✓ Updated: {current_db_filename} -> {matching_file}")
                    updated_count += 1
                else:
                    print(f"✗ Error: Could not find matching file for {current_db_filename}")
                    errors_count += 1
                    
        except Exception as e:
            print(f"✗ Error processing product {product.pro_name}: {str(e)}")
            errors_count += 1
    
    print("\nUpdate Summary:")
    print(f"Total products processed: {products.count()}")
    print(f"Already correct: {skipped_count}")
    print(f"Successfully updated: {updated_count}")
    print(f"Errors encountered: {errors_count}")

if __name__ == "__main__":
    print("Starting image name update process...")
    update_database_images()
    print("\nUpdate process completed!")
