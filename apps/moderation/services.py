import re
from django.utils import timezone
from datetime import timedelta
from .models import BlockedWord


def contains_blocked_word(text):
    """
    Retourne le premier mot bloqué trouvé dans le texte, ou None.
    La vérification est insensible à la casse.
    """
    words = BlockedWord.objects.values_list('word', flat=True)
    text_lower = text.lower()
    for word in words:
        # Recherche mot entier (évite les faux positifs)
        if re.search(r'\b' + re.escape(word.lower()) + r'\b', text_lower):
            return word
    return None


def check_post_for_moderation(post):
    """
    Vérifie le contenu d'un post contre la liste de mots bloqués.
    Si match → passe en pending_review avec auto_publish dans 24h.
    Retourne True si le post a été mis en attente.
    """
    full_text = f"{post.title} {post.content}"
    blocked = contains_blocked_word(full_text)

    if blocked:
        post.status = 'pending_review'
        post.save(update_fields=['status'])

        # Créer un signalement automatique pour l'admin
        from .models import Report
        Report.objects.create(
            post=post,
            reason='offensive',
            detail=f'Mot détecté automatiquement : "{blocked}"',
            auto_publish_at=timezone.now() + timedelta(hours=24),
        )
        return True

    return False
