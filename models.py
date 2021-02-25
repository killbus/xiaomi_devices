#!/usr/bin/env python3.7
"""Xiaomi Devices Models Info scrapper"""

import re
import json
from requests import get

def main(lang='en'):
    """
    scrapes Xiaomi devices md into json
    """
    DEVICES = {}

    filestem = 'xiaomi'
    if lang:
        filename = f'{filestem}_{lang}.md'
    else:
        filename = f'{filestem}.md'
    data = get("https://raw.githubusercontent.com/killbus/MobileModels/" +
               f"master/brands/{filename}").text
    data = [i for i in data.splitlines() if not str(i).startswith('#') and i]
    data = '\n'.join(data).replace('\n\n', '\n').replace('\n\n', '\n')
    devices = re.findall(r"\*(?:[\s\S]*?)\n\*|\*(?:[\s\S]*?)\Z", data, re.MULTILINE)
    for item in devices:
        info = {}
        details = item.split('*')
        details = [i for i in details if i]
        try:
            codename = details[0].split('(`')[1].split('`)')[0].strip()
        except IndexError:
            codename = ''
        try:
            internal = details[0].split('[`')[1].split('`]')[0].strip()
        except IndexError:
            internal = ''
        try:
            if ']' in details[0]:
                name = details[0].split(']')[1].split('(')[0].strip()
            else:
                name = details[0].split('(')[0].strip()
        except IndexError:
            name = details[0].split(':')[0].strip()
        models = details[1].replace('\n\n', '\n').strip().splitlines()
        info.update({"internal_name": internal})
        info.update({"name": name})
        models_ = {}
        for i in models:
            model_list = re.split(r'`\ +`', i.split(':')[0].strip())
            model_list = [i for i in model_list if i.strip().strip(r'`').strip()]
            for model in model_list:
                model = model.replace(r'`', '').strip()
                model_name = i.split(':')[1].strip()
                models_.update({model: model_name})
        info.update({"models": models_})
        try:
            if DEVICES[codename]:
                DEVICES[codename]['internal_name'] = f"{DEVICES[codename]['internal_name']}/{internal}" \
                    if DEVICES[codename]['internal_name'] != internal else internal
                DEVICES[codename]['name'] = f"{DEVICES[codename]['name']} / {name}"
                DEVICES[codename]['models'] = {**DEVICES[codename]['models'], **models_}
        except KeyError:
            DEVICES.update({codename: info})

    if lang:
        outf = f'models_{lang}.json'
    else:
        outf = 'models.json'
    with open(outf, 'w') as output:
        json.dump(DEVICES, output, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
    main('')
