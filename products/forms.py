from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model=ProductReview
        fields=["rating","comment"]
        widgets={
            "rating":forms.Select(
                choices=[
                    (1,"⭐1"),
                    (2,"⭐⭐2"),
                    (3,"⭐⭐⭐3"),
                    (4,"⭐⭐⭐⭐4"),
                    (5,"⭐⭐⭐⭐⭐5"),
                ],
                attrs={"class":"form-select"},
            ),
            "comment":forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":4,
                    "placeholder":"Write your review...",
                }
            ),
        }

    def clean_rating(self):
        rating=self.cleaned_data["rating"]

        if not 1 <= 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )    

        return rating 