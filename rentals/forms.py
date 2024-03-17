from django import forms



class NewRentalForm(forms.Form):
    student = forms.EmailField(required=True)
    book_name = forms.CharField(required=True)
    return_date = forms.DateField(required=True)


class NewStudentForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)