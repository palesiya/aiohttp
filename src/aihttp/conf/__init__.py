from dynaconf import Dynaconf
import pathlib


settings = Dynaconf(
    envvar_prefix="ARST",
    settings_files=[pathlib.Path(__file__).parent / '_conf.py'],
    enviroments=True,
    load_dotenv=True,
    env_switcher="ENV_FOR_ARST"
)
