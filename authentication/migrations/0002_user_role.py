
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('resident', 'Resident'), ('entrepreneur', 'Entrepreneur')], default='resident', max_length=20),
        ),
    ]
