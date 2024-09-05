# Generated by Django 4.1.13 on 2024-04-16 11:43
import threading

import django.contrib.postgres.search
from django.db import migrations

from common.util.common import sub_array
from common.util.ts_vecto_util import to_ts_vector
from dataset.models import Status
from embedding.models import Embedding


def update_embedding_search_vector(embedding, paragraph_list):
    paragraphs = [paragraph for paragraph in paragraph_list if paragraph.id == embedding.get('paragraph')]
    if len(paragraphs) > 0:
        content = paragraphs[0].title + paragraphs[0].content
        return Embedding(id=embedding.get('id'), search_vector=to_ts_vector(content))
    return Embedding(id=embedding.get('id'), search_vector="")


def save_keywords(apps, schema_editor):
    try:
        document = apps.get_model("dataset", "Document")
        embedding = apps.get_model("embedding", "Embedding")
        paragraph = apps.get_model('dataset', 'Paragraph')
        db_alias = schema_editor.connection.alias
        document_list = document.objects.using(db_alias).all()
        for document in document_list:
            document.status = Status.embedding
            document.save()
            paragraph_list = paragraph.objects.using(db_alias).filter(document=document).all()
            embedding_list = embedding.objects.using(db_alias).filter(document=document).values('id', 'search_vector',
                                                                                                'paragraph')
            embedding_update_list = [update_embedding_search_vector(embedding, paragraph_list) for embedding
                                     in embedding_list]
            child_array = sub_array(embedding_update_list, 50)
            for c in child_array:
                try:
                    embedding.objects.using(db_alias).bulk_update(c, ['search_vector'])
                except Exception as e:
                    print(e)
            document.status = Status.success
            document.save()
    except Exception as e:
        print(e)


def async_save_keywords(apps, schema_editor):
    thread = threading.Thread(target=save_keywords, args=(apps, schema_editor))
    thread.start()


class Migration(migrations.Migration):
    dependencies = [
        ('embedding', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='embedding',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(default='', verbose_name='分词'),
        ),
        migrations.RunPython(async_save_keywords)
    ]
