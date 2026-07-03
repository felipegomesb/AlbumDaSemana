from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0005_add_is_admin_to_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='user_bio',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_avatar',
            field=models.FileField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]