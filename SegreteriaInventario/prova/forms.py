# -*- coding: utf-8 -*-

from django import forms


class PictureForm(forms.Form):
	# foto da caricare
    picture = forms.FileField(
        label='Select a file'
    )
    # id dell'item a cui appartiene la foto
    id = forms.IntegerField(widget=forms.HiddenInput())