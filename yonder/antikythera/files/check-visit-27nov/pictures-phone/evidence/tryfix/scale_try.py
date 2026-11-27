"""The two trial pictures scaled to 350 pixels wide, side by side with the pictures as drawn (left: as drawn; right: trial)."""
from PIL import Image
HERE = '/home/agent3/site/check-pictures-phone'
for old, new, out in (('/home/agent3/site/build/img/dial-kept-phone.png', f'{HERE}/tryfix/dial-kept-phone-try.png', f'{HERE}/tryfix/dial-kept-both-350.png'),
                      ('/home/agent3/site/build/img/handshake-popsize-phone.png', f'{HERE}/tryfix/handshake-popsize-phone-try.png', f'{HERE}/tryfix/handshake-popsize-both-350.png')):
    a = Image.open(old).convert('RGB'); b = Image.open(new).convert('RGB')
    h = round(a.height * 350 / a.width)
    a = a.resize((350, h), Image.LANCZOS); b = b.resize((350, h), Image.LANCZOS)
    both = Image.new('RGB', (720, h), (255, 255, 255)); both.paste(a, (0, 0)); both.paste(b, (370, 0)); both.save(out)
    print('written', out, both.size)
