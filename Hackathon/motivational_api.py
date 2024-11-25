import requests

class MotivationalAPI:
    @staticmethod
    def fetch_quote():
        """Fetch a motivational quote from an API."""
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=10)
            response.raise_for_status()  # Vérifie si la réponse HTTP est valide (200 OK)
            if response.status_code == 200:
                quote = response.json()[0]['q']  # Accès à la citation dans la réponse JSON
                return quote
        except requests.exceptions.RequestException as e:
            print(f"Error fetching quote: {e}")
            return "Keep going, you're doing great!"  # Message de repli en cas d'erreur




