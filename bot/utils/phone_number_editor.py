import re


def phone_is_match(phone_number: str) -> bool:
    pattern = r'(\+7|8)[ (]?\(? ?(\d{3})[ )]?\)? ?(\d{3})(\-| )?(\d{2})(\-| )?(\d{2})'
    return bool(re.match(pattern, phone_number))


def phone_format_editor(phone_number: str):
    if phone_is_match(phone_number=phone_number):
        phone = ''.join(re.findall(r'[\d]', phone_number))
        phone = phone[::-1]
        formatted_phone = f'{phone[:2]}-{phone[2:4]}-{phone[4:7]} ){phone[7:10]}( 7+'
        return formatted_phone[::-1]
    return False
