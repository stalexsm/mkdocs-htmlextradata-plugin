import json
import logging
import os
from itertools import chain
from pathlib import Path

import yaml
from mkdocs.config import config_options as co
from mkdocs.plugins import BasePlugin

log = logging.getLogger(__name__)


class HtmlExtraDataPlugin(BasePlugin):
    """Данный плагин парсит данные в папке и добавляет в контекст приложения,
    чтобы потом можно было обработать в шаболоне."""

    config_scheme = (("data", co.Type(str, default="_extradata")),)

    def _add_data_in_context(self, config, namespace, data):
        """Добавим данные в контекст"""

        config[namespace] = data

    def on_pre_build(self, config):
        """Обработка данных и заполняем конфиг"""

        source_folders = self.config.data.get("data", [])
        base_path = os.path.dirname(self.config.config_file_path)
        if isinstance(source_folders, str):
            source_folders = [
                f"{base_path}/{dir_}" for dir_ in source_folders.split(",")
            ]

        if not source_folders:
            source_folders = []
            for datadir in [
                os.path.dirname(self.config.config_file_path),
                self.config.docs_dir,
            ]:
                ds_folder = os.path.join(datadir, "_extradata")
                if os.path.exists(ds_folder):
                    source_folders.append(ds_folder)

        if not source_folders:
            return

        for ds_folder in source_folders:
            if os.path.exists(ds_folder):
                path = Path(ds_folder)
                for filename in chain(
                    path.glob("**/*.yaml"),
                    path.glob("**/*.yml"),
                    path.glob("**/*.json"),
                ):
                    namespace = os.path.splitext(os.path.relpath(filename, ds_folder))[
                        0
                    ]
                    self._add_data_in_context(
                        config,
                        namespace,
                        (
                            yaml.load(filename.read_bytes(), Loader=yaml.FullLoader)
                            if filename.suffix in [".yml", ".yaml"]
                            else json.loads(filename.read_bytes())
                        ),
                    )

    def on_page_context(self, context, *, page, config, nav):
        """Контекст для страницы"""

        namespace = page.url.rstrip("/").split("/").pop()
        if namespace in config:
            context["extradata"] = config[namespace]  # type: ignore

        return context
