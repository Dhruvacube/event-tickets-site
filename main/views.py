from django.shortcuts import render

# Create your views here.
class Games(models.Model):
    name = models.CharField(max_lenth=200, help_text=_('The name of the game'))
    short_description = models.TextField(help_text=_('About this short event, better keep it in between 100 characters'), validators=[MinLengthValidator(13),MaxLengthValidator(100)])
    long_description = models.TextField(help_text=_('Here explain everything'))
    image_url = models.URLField(help_text=_('Url of the game image'))
    platform = models.CharField(max_length=11,choices=(('a','ALL'),('m','Mobile'),('p','PC'),('pc','Play Station')), default='A')
    solo_entry = models.IntegerField(help_text='Enter the Solo entry price')
    squad_entry = models.IntegerField(help_text='Enter the Sqaud entry price')
    
    def __str__(self):
        return self.name
