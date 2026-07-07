from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0006_usuario_profile_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='musica',
            name='adicionado_por_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='album',
            name='adicionado_por_admin',
            field=models.BooleanField(default=False),
        ),
    ]
