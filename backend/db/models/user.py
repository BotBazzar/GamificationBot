from django.db import models


class User(models.Model):
    chat_id = models.CharField(max_length=255,unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    score = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    has_spun = models.BooleanField(default=False)
    prize = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_id

    @classmethod
    def get_available_prizes(cls):
        """Get count of available prizes for each type"""
        prizes = {
            0: 8 - cls.objects.filter(prize=0).count(),
            1: 8 - cls.objects.filter(prize=1).count(),
            2: 8 - cls.objects.filter(prize=2).count()
        }
        return prizes

    @classmethod
    def assign_prize(cls, user):
        """Assign a random prize to a user"""
        if user.has_spun:
            return False

        available_prizes = cls.get_available_prizes()
        total_available = sum(available_prizes.values())
        
        if total_available == 0:
            return False

        # Create a weighted list of available prizes
        prize_list = []
        for prize_type, count in available_prizes.items():
            prize_list.extend([prize_type] * count)

        # Randomly select a prize from available ones
        import random
        selected_prize = random.choice(prize_list)

        # Assign the prize
        user.prize = selected_prize
        user.save()
        return True
