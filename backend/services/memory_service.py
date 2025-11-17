from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from database import models

PreferenceDict = Dict[str, str]


def get_or_create_user(db: Session, external_user_id: str, display_name: Optional[str] = None) -> models.User:
	user = db.query(models.User).filter(models.User.external_id == external_user_id).one_or_none()
	if user:
		return user
	user = models.User(external_id=external_user_id, display_name=display_name)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


def set_user_preferences(db: Session, user_id: int, prefs: PreferenceDict) -> List[models.UserPreference]:
	# Upsert by (user_id, key)
	existing = (
		db.query(models.UserPreference)
		.filter(models.UserPreference.user_id == user_id)
		.all()
	)
	key_to_pref = {p.key: p for p in existing}
	results: List[models.UserPreference] = []
	for key, value in prefs.items():
		if key in key_to_pref:
			p = key_to_pref[key]
			p.value = value
			results.append(p)
		else:
			p = models.UserPreference(user_id=user_id, key=key, value=value)
			db.add(p)
			results.append(p)
	db.commit()
	return results


def get_user_preferences(db: Session, user_id: int) -> PreferenceDict:
	prefs = (
		db.query(models.UserPreference)
		.filter(models.UserPreference.user_id == user_id)
		.all()
	)
	return {p.key: p.value for p in prefs}


def summarize_preferences(prefs: PreferenceDict) -> str:
	if not prefs:
		return "No explicit preferences."
	parts = []
	for key, value in prefs.items():
		parts.append(f"{key}: {value}")
	return "; ".join(parts)



