from dynaconf import Dynaconf
import pathlib

__all__ = ("settings", )

settings = Dynaconf(
    envvar_prefix="ARST",
    settings_files=[pathlib.Path(__file__).parent / "_conf.p"],
    env_switcer="ENV_FOR_ARST",
    environments=True,
    load_dotenv=True,
)
