from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0003_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='album',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='musica',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='musica',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]