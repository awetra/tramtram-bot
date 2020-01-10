import requests


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.request_base_url = f'https://api.telegram.org/bot{token}/'

    def set_webhook(self, webhook_url):
        requests.post(
            f'{self.request_base_url}setWebhook',
            data={
                'url': webhook_url
            }
        )

    def get_webhook_info(self):
        return requests.post(f'{self.request_base_url}getWebhookInfo').json()

    def send_message(self, data, html=True):
        if html:
            data['parse_mode'] = 'HTML'
        requests.post(
            f'{self.request_base_url}sendMessage',
            data=data
        )

    def edit_message_text(self, data, html=True):
        if html:
            data['parse_mode'] = 'HTML'
        requests.post(
            f'{self.request_base_url}editMessageText',
            data=data
        )

