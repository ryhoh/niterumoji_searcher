import subprocess


def gen(code):
    try:
        c = chr(code)
    except ValueError as e:
        print('[INFO] ValueError thrown in code %x' % code)
        return None

    if c in ('"', "'", '\\', '`'):
        c = "\\" + c
    subprocess.call('echo "%s" | ./cmd2png.sh output/%x.png' % (c, code), shell=True)


for code in range(0x0021, 0x2E45):
    gen(code)

for code in range(0xA000, 0xABFA):
    gen(code)

for code in range(0xFF01, 0xFFEF):
    gen(code)
