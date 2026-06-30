from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0004_item_likes_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]