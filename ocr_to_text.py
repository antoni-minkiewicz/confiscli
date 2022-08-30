"""
This script is taken and amended from: https://github.com/writecrow/ocr2text

MIT License

Copyright (c) 2017 CROW

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import os
import shutil
import errno
import subprocess
from tempfile import mkdtemp


try:
    from PIL import Image
except ImportError:
    print('Error: You need to install the "Image" package. Type the following:')
    print('pip install Image')

try:
    import pytesseract
except ImportError:
    print('Error: You need to install the "pytesseract" package. Type the following:')
    print('pip install pytesseract')
    exit()

try:
    from pdf2image import convert_from_path, convert_from_bytes
except ImportError:
    print('Error: You need to install the "pdf2image" package. Type the following:')
    print('pip install pdf2image')
    exit()

class OcrToText():
    def __init__(self):
        pass
    
    def conversion(self, source='', destination=''):
        
        count = 0
        
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if source == '':
            source = dir_path
            
        if destination == '':
            destination = dir_path

        if (os.path.exists(source)):
            if (os.path.isdir(source)):
                print('source must be a single file')
            elif os.path.isfile(source):  
                filepath, fullfile = os.path.split(source)
                filename, file_extension = os.path.splitext(fullfile)
                if (file_extension.lower() == '.pdf'):
                    # destination_file = os.path.join(destination, filename + '.txt')
                    count = self.convert(source, destination, count)
                    print('File converted')
                    return destination

        else:
            print('The path ' + source + 'seems to be invalid')
            
        
            
    
    def convert(self, sourcefile, destination_file, count):
        text = self.extract_tesseract(sourcefile)
        with open(destination_file, 'w', encoding='utf-8') as f_out:
            f_out.write(text)
        print()
        print('Converted ' + sourcefile)
        count += 1
        return count
    
    def run(self, args):
        # run a subprocess and put the stdout and stderr on the pipe object
        try:
            pipe = subprocess.Popen(
                args,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except OSError as e:
            if e.errno == errno.ENOENT:
                # File not found.
                # This is equivalent to getting exitcode 127 from sh
                raise exceptions.ShellError(
                    ' '.join(args), 127, '', '',
                )

        # pipe.wait() ends up hanging on large files. using
        # pipe.communicate appears to avoid this issue
        stdout, stderr = pipe.communicate()

        # if pipe is busted, raise an error (unlike Fabric)
        if pipe.returncode != 0:
            raise exceptions.ShellError(
                ' '.join(args), pipe.returncode, stdout, stderr,
            )

        return stdout, stderr


    def extract_tesseract(self, filename):
            temp_dir = mkdtemp()
            base = os.path.join(temp_dir, 'conv')
            contents = []
            try:
                stdout, _ = self.run(['pdftoppm', filename, base])

                for page in sorted(os.listdir(temp_dir)):
                    page_path = os.path.join(temp_dir, page)
                    page_content = pytesseract.image_to_string(Image.open(page_path))
                    contents.append(page_content)
                return ''.join(contents)
            finally:
                shutil.rmtree(temp_dir)