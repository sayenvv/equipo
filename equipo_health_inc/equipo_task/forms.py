from tkinter import Widget
from django import forms
from ckeditor.widgets import CKEditorWidget


class consultation_Form(forms.Form):
    clinic_name = forms.CharField(max_length=200)
    clinic_logo = forms.CharField(max_length=200)
    physician_name = forms.CharField(max_length=200)
    physician_contact = forms.CharField(max_length=200)
    patient_firstname = forms.CharField(max_length=200)
    patient_lastname = forms.CharField(max_length=200)
    patient_dob = forms.CharField(max_length=200)
    patient_contact = forms.CharField(max_length=200)
    cheif_complaint = forms.CharField(widget=CKEditorWidget(),required=False)
    consultation_note = forms.CharField(widget=CKEditorWidget(),required=False)


    def __init__(self, *args, **kwargs):
        super(consultation_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})


