from app.infrastructure.notif.notification_provider import (
    EmailProvider, 
    SMSProvider, 
    PushProvider
)

class FabriqueNotification:
    """
    DESIGN PATTERN : SIMPLE FACTORY
    Permet de créer le fournisseur de notification approprié sans exposer
    la logique d'instanciation complexe au service applicatif.
    """

    @staticmethod
    def notifier(canal: str):
        """
        Retourne une instance du provider correspondant au canal choisi.
        :param canal: 'email', 'sms' ou 'push'
        :return: Une instance de NotificationProvider
        """
        canaux = {
            "email": EmailProvider,
            "sms": SMSProvider,
            "push": PushProvider
        }

        # Normalisation de l'entrée (minuscules et suppression d'espaces)
        canal_normalise = canal.strip().lower()

        if canal_normalise in canaux:
            return canaux[canal_normalise]()
        else:
            raise ValueError(f"⚠️ Canal de notification non supporté : {canal}")

# Exemple d'utilisation dans un service :
# FabriqueNotification.notifier("email").envoyer(user_id, "Votre commande est prête !")