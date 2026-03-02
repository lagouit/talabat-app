class NotificationEmail(Notification):
    def envoyer(self, u_id):
        print(f"📧 [EMAIL] envoyé à l'utilisateur {u_id} : {self._message}")

class NotificationSMS(Notification):
    def envoyer(self, u_id):
        print(f"📱 [SMS] envoyé à l'utilisateur {u_id} : {self._message}")

class FabriqueNotification:
    @staticmethod
    def notifier(type_notif: str, message: str):
        if type_notif == "email":
            return NotificationEmail(message)
        elif type_notif == "sms":
            return NotificationSMS(message)
        return None