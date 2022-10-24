import re


def fio_is_match(fio: str) -> bool:
    pattern = r'^[a-zA-Zа-яА-Я]+(-[a-zA-Zа-яА-Я]+)? [a-zA-Zа-яА-Я]+(-[a-zA-Zа-яА-Я]+)?$'
    return bool(re.match(pattern, fio))


def fio_format_editor(fio: str):
    if fio_is_match(fio):
        name, surname = fio.split()
        name = '-'.join([_.capitalize() for _ in name.split('-')])
        surname = '-'.join([_.capitalize() for _ in surname.split('-')])
        fio = ' '.join([_ for _ in (name, surname)])
        return fio
    return False

