import os

project_root = '.'  # current folder

for root, dirs, files in os.walk(project_root):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                content = f.read()
            # remove BOM if present
            if content.startswith(b'\xef\xbb\xbf'):
                content = content[3:]
                print(f'Removed BOM: {path}')
            # ensure utf-8 encoding
            try:
                content.decode('utf-8')
            except UnicodeDecodeError:
                # try utf-16 and re-encode
                content = content.decode('utf-16').encode('utf-8')
                print(f'Converted UTF-16 to UTF-8: {path}')
            with open(path, 'wb') as f:
                f.write(content)
