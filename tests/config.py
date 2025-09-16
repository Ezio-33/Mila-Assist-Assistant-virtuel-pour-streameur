"""
Configuration centralisée pour Mila Assist.

Objectifs:
- Par défaut, utiliser l'API hébergée sur le NAS (pas de DB locale nécessaire).
- Exposer une seule variable (API_URL) facile à modifier en cas de migration.
- Permettre un mode hors-ligne sans base de données (USE_API=false, USE_DB=false).

Surcharges possibles via variables d'environnement (.env) sans toucher au code.
"""

import os
from dotenv import load_dotenv

# Charger automatiquement le .env à la racine du projet si présent
load_dotenv()


def str_to_bool(val: str, default: bool = False) -> bool:
	if val is None:
		return default
	return str(val).strip().lower() in {"1", "true", "yes", "on"}


class Config:
	"""Conteneur des variables de configuration utilisées par l'app web."""

	# Par défaut: on passe par le NAS (API), pas de DB locale nécessaire
	USE_API: bool
	USE_DB: bool

	# Adresse API unique à modifier en cas de migration
	API_URL: str
	API_KEY: str
	USE_LEGACY_FALLBACK: bool

	# Flask
	HOST: str
	PORT: int
	DEBUG: bool
	SECRET_KEY: str

	def __init__(self) -> None:
		# Valeurs par défaut sécurisées
		default_api_url = os.getenv(
			"API_URL",
			# Valeur par défaut générique
			os.getenv("NAS_API_URL", "http://localhost:5000/api"),
		)

		self.USE_API = str_to_bool(os.getenv("USE_API"), default=True)
		self.USE_DB = str_to_bool(os.getenv("USE_DB"), default=True)  # Activé par défaut pour utiliser la base française

		self.API_URL = default_api_url
		self.API_KEY = os.getenv("API_KEY", os.getenv("DEFAULT_API_KEY", "dev_key_123456789"))
		self.USE_LEGACY_FALLBACK = str_to_bool(os.getenv("USE_LEGACY_FALLBACK"), default=False)

		self.HOST = os.getenv("HOST", "localhost")
		self.PORT = int(os.getenv("PORT", 5000))
		self.DEBUG = str_to_bool(os.getenv("DEBUG"), default=False)
		self.SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

		# TEMPORAIRE: Compatibilité pendant transition (à supprimer plus tard)
		self.RESPONSE_MODE = "simple"


# Instance unique utilisée par défaut
config = Config()


def reload_config() -> Config:
	"""Recharge la configuration depuis les variables d'environnement."""
	global config
	config = Config()
	return config
