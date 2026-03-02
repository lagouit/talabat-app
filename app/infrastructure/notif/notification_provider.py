from abc import ABC, abstractmethod

class NotificationProvider(ABC):
    """
    INTERFACE ABSTRAITE (Infrastructure)
    Définit le contrat pour tous les canaux de communication.
    """
    @abstractmethod
    def envoyer(self, destinataire_id: int, message: str):
        pass

class EmailProvider(NotificationProvider):
    """
    Simulateur d'envoi d'Email.
    Dans une version réelle, on utiliserait smtplib ou une API tierce.
    """
    def envoyer(self, destinataire_id: int, message: str):
        print(f"📧 [EMAIL] Envoi à l'utilisateur #{destinataire_id}...")
        print(f"   ✉️ Contenu : {message}")
        print("   ✅ Email expédié avec succès via le serveur SMTP.")

class SMSProvider(NotificationProvider):
    """
    Simulateur d'envoi de SMS.
    Dans une version réelle, on utiliserait l'API Twilio.
    """
    def envoyer(self, destinataire_id: int, message: str):
        print(f"📱 [SMS] Envoi au mobile de l'utilisateur #{destinataire_id}...")
        print(f"   💬 Message : {message}")
        print("   ✅ SMS délivré via la passerelle télécom.")

class PushProvider(NotificationProvider):
    """
    Simulateur de notification Push (Application Mobile).
    """
    def envoyer(self, destinataire_id: int, message: str):
        print(f"🔔 [PUSH] Notification envoyée sur l'appareil de #{destinataire_id}...")
        print(f"   📲 Titre : Talabat Update - {message}")