import os, struct
from tools.path import halflife

class PakFile:
    def __init__(self, filename):
        self.filename = filename
        self.files = {}
        self._read_pak_file()

    def _read_pak_file(self):
        with open(self.filename, 'rb') as f:
            header = f.read(12)
            if header[:4] != b'PACK':
                raise ValueError('Not a valid PAK file')

            (dir_offset, dir_length) = struct.unpack('ii', header[4:])
            f.seek(dir_offset)
            dir_data = f.read(dir_length)

            num_files = dir_length // 64
            for i in range(num_files):
                entry = dir_data[i*64:(i+1)*64]
                name = entry[:56].rstrip(b'\x00').decode('utf-8')
                (offset, length) = struct.unpack('ii', entry[56:])
                self.files[name] = (offset, length)

    def extract(self, extract_to):
        with open(self.filename, 'rb') as f:
            for name, (offset, length) in self.files.items():
                f.seek(offset)
                data = f.read(length)

                extract_path = os.path.join(extract_to, name)
                os.makedirs(os.path.dirname(extract_path), exist_ok=True)

                if os.path.exists(extract_path):
                    #print(f"[pak.py] {name} exists. skipping...")
                    continue

                with open(extract_path, 'wb') as out_file:
                    out_file.write(data)

                print(f"[extract_pak] Extracted {name} to {extract_path}")

def extract_pak( paks=[], mod='' ):
    for p in paks:
        if not p.endswith('.pak'):
            p = f'{p}.pak'
        pak = PakFile( f'{halflife}\{mod}\{p}' )
        pak.extract( f'{halflife}\{mod}\\' )
