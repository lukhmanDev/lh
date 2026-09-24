import os
import zipfile

source_dir = r"d:\projects\Lukman\backend\portfolio"
output_zip = r"d:\projects\Lukman\backend\portfolio.zip"

if os.path.exists(output_zip):
    os.remove(output_zip)

count = 0
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        # Exclude pycache and hidden cache directories
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.pytest_cache', '.git')]
        for file in files:
            if file.endswith('.pyc') or file == 'portfolio.zip':
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, source_dir)
            zipf.write(full_path, rel_path)
            count += 1

print(f"Successfully archived {count} files into {output_zip}")
