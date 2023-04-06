# MkDocs-htmlextradata-plugin

*Плагин MkDocs, который вводит дополнительную переменную `extradata` в html-шаблон. Данная переменная попадает в контекст страницы, если файл .yml называется так же ка странца .md*

## Установка

Установите пакет с помощью pip или poetry:

```bash
pip install htmlextradata

or

poetry add htmlextradata
```

Включите плагин в вашем "mkdocs.yml`:

```yaml
plugins:
    - search
    - htmlextradata
```

или

```yaml
plugins:
    - search
    - htmlextradata:
        data: path/to/datafiles
```

По умолчанию он будет искать в папке, где хранится ваш mkdocs.yml, и в папке docs другую папку с именем _extradata (т.е. ./docs/_extradata/mtrs.yaml), доступную в шаблоне как {{ extradata }}, если есть страница с таким именем.
