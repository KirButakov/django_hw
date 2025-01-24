from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'available', 'category']

    def check_forbidden_words(self, field_value):
        forbidden_words = Product.FORBIDDEN_WORDS
        for word in forbidden_words:
            if word.lower() in field_value.lower():
                raise forms.ValidationError(f'Значение не может содержать слово: {word}')
        return field_value

    def clean_name(self):
        name = self.cleaned_data['name']
        return self.check_forbidden_words(name)

    def clean_description(self):
        description = self.cleaned_data['description']
        return self.check_forbidden_words(description)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)


        if not self.instance.pk:
            self.fields['available'].initial = True


        self.fields['available'].required = False


        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
