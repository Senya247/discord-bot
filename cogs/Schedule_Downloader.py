import os
import sys
import requests
import fitz
from datetime import date
sys.path.append("/home/runner/discord-bot/cogs")
from colors import colors
from PIL import Image
import PIL.ImageOps


def withoutO(number):

    if str(number)[0] == '0':
        return str(number)[1:]
    return (str(number))


allowed_files = "Movesets.txt"

shortmonths = {
    'January': 'Jan',
    'February': 'Feb',
    'March': 'Mar',
    'April': 'Apr',
    'May': 'May',
    'June': 'Jun',
    'July': 'Jul',
    'August': 'Aug',
    'September': 'Sep',
    'October': 'Oct',
    'November': 'Nov',
    'December': 'Dec'
}
months = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

Month = months[str(date.today()).split('-')[1]]
Date = str(date.today()).split('-')[-1]

school_url = 'http://www.sanskritischool.edu.in/News/'
# list of possible pages
hits = [
    school_url + shortmonths[Month] + '%20' + withoutO(str(Date)) + '.pdf',
    school_url + (shortmonths[Month]).upper() + "%20 " + Date + ".pdf",
    school_url + Month + '%20' + str(Date) + '.pdf', school_url +
    shortmonths[Month].upper() + '%20' + withoutO(str(Date)) + '.pdf',
    school_url + Month.upper() + '%20' + str(Date) + '.pdf'
]

Downloaded = False

files = [f for f in os.listdir('/home/runner/discord-bot/cogs')]
print(files)
for file in os.listdir(
        '/home/runner/discord-bot/cogs/'
):  #[f for f in os.listdir('cogs/') if os.path.isfile(f)]:
    if Date in file and 'png' in file:
        Downloaded = True
    else:
        if 'py' not in file and file not in allowed_files:
            print(f'{file}')
            os.remove(f'/home/runner/discord-bot/cogs/{file}')

if not Downloaded:
    pdf = None
    for i in range(len(hits)):
        pdf = requests.get(hits[i])
        try:
            pdf.raise_for_status()
            break
        except requests.exceptions.HTTPError:
            continue

    try:
        pdf.raise_for_status()
        with open(f'cogs/{Month}{Date}.pdf', 'wb') as f:
            for chunk in pdf.iter_content(100):
                f.write(chunk)
        print(
            f'{colors.OKGREEN}DOWNLOADED SCHEDULE WITHOUT ERROR{colors.ENDC}')
        pdffile = f"cogs/{Month}{Date}.pdf"
        doc = fitz.open(pdffile)
        page = doc.loadPage(0)  # number of page
        pix = page.getPixmap(matrix=fitz.Matrix(2, 2))
        output = f"cogs/{Month}{Date}.png"
        pix.writePNG(output)
        image = Image.open(f'cogs/{Month}{Date}.png')

        inverted_image = PIL.ImageOps.invert(image)
        os.remove(f'cogs/{Month}{Date}.pdf')
        os.remove(f'cogs/{Month}{Date}.png')

        inverted_image.save(f'cogs/{Month}{Date}.png')
    except requests.exceptions.HTTPError:
        print(f'{colors.ERROR}DOWNLOAD SCHEDULE FAILED{colors.ENDC}')
else:
    print(f'{colors.OKGREEN}SCHEDULE ALREADY DOWNLOADED {colors.ENDC}')
