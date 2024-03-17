from django.utils import timezone

def compute_price(date, pages):
    current_date = timezone.now().date()
    if date < current_date:
        raise ValueError('Date cannot be in the past')
    
    if date.month == current_date.month:
        return  0
    else:
        return int(pages) / 100