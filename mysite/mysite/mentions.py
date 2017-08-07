# from these instructions: https://github.com/ivirabyan/django-mentions 

from mentions import Provider

class UserProvider(Provider):
    model = User
    
    def get_title(self, obj):
        return obj.username
    
    def search(self, request, term):
        return self.get_queryset().filter(username__istartswith=term)
