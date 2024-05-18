import django.utils.timezone
from django.db import migrations, models
from django.utils import timezone


def convert_int_to_datetime(apps, schema_editor):
    Habit = apps.get_model('habits', 'Habit')
    for habit in Habit.objects.all():
        habit.complete_time_tmp = timezone.datetime.fromtimestamp(habit.complete_time)
        habit.save()


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_alter_habit_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='complete_time_tmp',
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(convert_int_to_datetime),
        migrations.RemoveField(
            model_name='habit',
            name='complete_time',
        ),
        migrations.RenameField(
            model_name='habit',
            old_name='complete_time_tmp',
            new_name='complete_time',
        ),
    ]
