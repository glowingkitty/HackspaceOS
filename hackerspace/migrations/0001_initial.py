# Generated by Django 3.0 on 2019-12-07 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consensus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('url_discourse', models.URLField(blank=True, null=True, verbose_name='Discourse URL')),
                ('str_status', models.CharField(choices=[('new', 'New'), ('passed_1', 'Meeting 1 passed'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('archived', 'Archived')], default='new', max_length=250, verbose_name='Status')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_error_code', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('str_name', models.CharField(blank=True, max_length=250, null=True)),
                ('int_count', models.IntegerField(default=0)),
                ('text_description', models.TextField(blank=True, null=True)),
                ('text_description_no_numbers', models.TextField(blank=True, null=True)),
                ('text_context', models.TextField(blank=True, null=True)),
                ('boolean_fixed', models.BooleanField(default=False)),
                ('text_origins', models.TextField(blank=True, null=True)),
                ('text_dateUNIXtimes', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='published')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='last_updated')),
            ],
        ),
        migrations.CreateModel(
            name='Guilde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_slug', models.CharField(blank=True, max_length=250, null=True)),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('url_featured_photo', models.URLField(blank=True, null=True, verbose_name='Photo URL')),
                ('url_wiki', models.URLField(blank=True, null=True, verbose_name='Wiki URL')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('url_featured_photo', models.URLField(blank=True, null=True, verbose_name='Photo URL')),
                ('url_discourse', models.URLField(blank=True, null=True, verbose_name='Discourse URL')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('url_image', models.URLField(blank=True, max_length=250, null=True, verbose_name='Image URL')),
                ('url_post', models.URLField(blank=True, max_length=250, null=True, verbose_name='Post URL')),
                ('str_source', models.CharField(blank=True, max_length=250, null=True, verbose_name='Source')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('url_discourse', models.URLField(blank=True, null=True, verbose_name='Discourse URL')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
                ('one_person', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_wishes_person', to='hackerspace.Person', verbose_name='Guilde')),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_slug', models.CharField(blank=True, max_length=250, null=True)),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('url_featured_photo', models.URLField(blank=True, null=True, verbose_name='Photo URL')),
                ('url_wiki', models.URLField(blank=True, null=True, verbose_name='Wiki URL')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
                ('one_guilde', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_spaces_guilde', to='hackerspace.Guilde', verbose_name='Guilde')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('url_featured_photo', models.URLField(blank=True, null=True, verbose_name='Photo URL')),
                ('url_discourse', models.URLField(blank=True, null=True, verbose_name='Discourse URL')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
                ('one_creator', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_project_creator', to='hackerspace.Person', verbose_name='Creator')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_date', models.TextField(blank=True, null=True)),
                ('text_notes', models.TextField(blank=True, null=True)),
                ('text_main_topics', models.TextField(blank=True, null=True)),
                ('text_keywords', models.TextField(blank=True, null=True)),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
                ('many_consensus_items', models.ManyToManyField(blank=True, related_name='m_consensus_items', to='hackerspace.Consensus')),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_slug', models.CharField(blank=True, max_length=250, null=True)),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('url_featured_photo', models.URLField(blank=True, null=True, verbose_name='Photo URL')),
                ('url_wiki', models.URLField(blank=True, null=True, verbose_name='Wiki URL')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
                ('one_guilde', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_machine_guilde', to='hackerspace.Guilde', verbose_name='Guilde')),
                ('one_space', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_machine_space', to='hackerspace.Space', verbose_name='Space')),
            ],
        ),
        migrations.AddField(
            model_name='guilde',
            name='many_members',
            field=models.ManyToManyField(blank=True, related_name='m_members', to='hackerspace.Person', verbose_name='Members'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('str_slug', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('boolean_approved', models.BooleanField(default=True)),
                ('int_UNIXtime_event_start', models.IntegerField(blank=True, null=True, verbose_name='Event start (UNIX time)')),
                ('int_minutes_duration', models.IntegerField(default=60, verbose_name='Duration in minutes')),
                ('int_UNIXtime_event_end', models.IntegerField(blank=True, null=True, verbose_name='Event end (UNIX time)')),
                ('url_featured_photo', models.URLField(blank=True, null=True, verbose_name='Photo URL')),
                ('text_description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('str_location', models.CharField(default='TAMI<br>Kibbutz Galuyot 45<br6655031, Tel Aviv, Tel Aviv-Yafo, IL', max_length=250, verbose_name='Location')),
                ('float_lat', models.FloatField(blank=True, default=32.0523183, null=True, verbose_name='Lat')),
                ('float_lon', models.FloatField(blank=True, default=34.7678285, null=True, verbose_name='Lon')),
                ('str_series_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='Series ID')),
                ('int_series_startUNIX', models.IntegerField(blank=True, null=True, verbose_name='Series Start (UNIX time)')),
                ('int_series_endUNIX', models.IntegerField(blank=True, null=True, verbose_name='Series End (UNIX time)')),
                ('str_series_repeat_how_often', models.CharField(blank=True, choices=[('weekly', 'weekly'), ('biweekly', 'biweekly'), ('monthly', 'monthly')], max_length=50, null=True, verbose_name='Series How often repeating?')),
                ('text_series_timing', models.TextField(blank=True, null=True)),
                ('str_crowd_size', models.CharField(choices=[('small', 'Up to 10 people'), ('medium', 'Up to 20 people'), ('large', 'More than 20 people')], default='small', max_length=250, verbose_name='Expected crowd size')),
                ('str_welcomer', models.CharField(blank=True, max_length=250, null=True, verbose_name='(for large events) Who welcomes people at the door?')),
                ('url_meetup_event', models.URLField(blank=True, max_length=250, null=True, verbose_name='Meetup URL')),
                ('url_discourse_event', models.URLField(blank=True, max_length=250, null=True, verbose_name='discourse URL')),
                ('url_discourse_wish', models.URLField(blank=True, max_length=250, null=True, verbose_name='discourse wish URL')),
                ('int_UNIXtime_created', models.IntegerField(blank=True, null=True)),
                ('int_UNIXtime_updated', models.IntegerField(blank=True, null=True)),
                ('str_timezone', models.CharField(blank=True, default='Asia/Jerusalem', max_length=100, null=True, verbose_name='Timezone')),
                ('many_hosts', models.ManyToManyField(blank=True, related_name='m_persons', to='hackerspace.Person', verbose_name='Hosts')),
                ('one_guilde', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_guilde', to='hackerspace.Guilde', verbose_name='Guilde')),
                ('one_space', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_space', to='hackerspace.Space', verbose_name='Space')),
            ],
        ),
        migrations.AddField(
            model_name='consensus',
            name='one_creator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_consensus_creator', to='hackerspace.Person', verbose_name='Creator'),
        ),
    ]
